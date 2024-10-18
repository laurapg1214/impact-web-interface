from apps.events.models import Event
from apps.attendees.models import Facilitator, Participant, EventAttendee
from apps.questions.models import Question
from django.apps import apps
from django.shortcuts import render
from rest_framework import serializers, viewsets
import uuid


# encapsulated views.py functionality with exception rendering custom error page
def get_object_or_error(
        request, 
        model, 
        object_id, 
        template_path, 
        extra_context=None, 
        event_name=None
        ):
    try:
        object = model.objects.get(pk=object_id)
        context_key = model.__name__.lower()
        context = {context_key: object}

        # merge extra_context, if provided, into context
        if extra_context:
            context.update(extra_context)

        return render(request, f"obwob/{template_path}", context)
    
    except model.DoesNotExist:
        requested_object = model.__name__.lower()
        return render(request, "obwob/404.html", {
            'error_message': f'Sorry, that {requested_object} does not exist.'
        })
    

### MODELS LIST & FUNCTIONS for API layer automation of serializers, viewsets & URL registrations

MODELS_LIST = [
    # app_label, model_name
    ('attendees', 'Facilitator'),
    ('attendees', 'Participant'),
    #('attendees', 'Demographics'),
    #('attendees', 'CustomDemographicField'),
    #('attendees', 'CustomDemographicValue'),
    ('organizations', 'Organization'),
    ('coordinators', 'Coordinator'),
    ('questions', 'Question'),
    ('events', 'Event'),
    ('attendees', 'EventAttendee'),
    ]


CUSTOM_SERIALIZER_MODELS = [
    'EventAttendee',
    'Event',
]


# dynamically import models from specified app
def get_model(app_label, model_name):
    try:
        return apps.get_model(app_label, model_name)
    except LookupError:
        raise ValueError(f"Model {model_name} in app {app_label} not found.")


### GENERATE CUSTOM SERIALIZERS & VIEWSETS (standard serialization & viewset generation below) ###

# function to call custom serializers generation within generate serializers & viewsets functions below
# keep updated whenever custom serializer or viewset function added
def use_custom_serializer(model_name, serializers_dict):
    if model_name == 'EventAttendee':
        return event_attendee_create_serializer() 
    elif model_name == 'Event':
        return event_create_serializer(serializers_dict)
    
    
def use_custom_viewset(model_name, serializers_dict):
    if model_name == 'EventAttendee':
        return event_attendee_create_viewset()
    elif model_name == 'Event':
        return event_create_viewset(serializers_dict)
    

### CUSTOM SERIALIZER FUNCTIONS ###

# dynamically add attendees during live event
def event_attendee_create_serializer(): 
    class EventAttendeeSerializer(serializers.ModelSerializer):
        class Meta:
            model = Event
            fields = ['facilitators', 'participants']
    

        def update(self, instance, validated_data):
            facilitators_data = validated_data.pop('facilitators', [])
            participants_data = validated_data.pop('participants', [])

            # extract attendee model and type to avoid code duplication
            if facilitators_data:
                model = Participant
                attendees_data = participants_data
            else:
                model = Facilitator
                attendees_data = facilitators_data

            # create lists for both existing and new facilitators & participants, 
            # for bulk adding to minimize db hits
            attendees_to_create = []
            attendees_to_add = []

            for attendee_data in attendees_data:
                # automatically assign a unique identifier if not provided
                unique_id = attendee_data.get('unique_id') or str(uuid.uuid4())
                
                # find or create the facilitator/participant
                attendee, created = model.objects.get_or_create(
                    unique_id=unique_id,
                    defaults={
                        'first_name': attendee_data.get('first_name', ''),
                        'last_name': attendee_data.get('last_name', '')
                    }
                )
                
                if created:
                    attendees_to_create.append(attendee)
                else:
                    attendees_to_add.append(attendee)

            # bulk create new attendees
            model.objects.bulk_create(attendees_to_create)

            # add new and existing attendees to the event
            if attendees_to_create or attendees_to_add:
                instance.attendees.add(*attendees_to_create, *attendees_to_add)
            
            return instance
        
    return EventAttendeeSerializer
    

def event_create_serializer(serializers_dict):
    class EventSerializer(serializers.ModelSerializer):
        attendees = serializers_dict.get(('attendees', 'EventAttendee'))(many=True)
        questions = serializers_dict.get(('questions', 'Question'))(many=True)

        class Meta:
            model = Event
            fields = '__all__'

        def create(self, validated_data):
            # extract attendees and questions data if present
            attendees_data = validated_data.pop('attendees', []) 
            questions_data = validated_data.pop('questions', [])

            # create the event object
            event = Event.objects.create(**validated_data) 

            # prepare lists for bulk creation
            attendees_to_add = []
            questions_to_add = []

            # add attendees to the event
            for attendee_data in attendees_data:
                # distinguish between participant and facilitator
                attendee_type = attendee_data.get('attendee_type')
                if attendee_type == 'participant':
                    attendee, created = Participant.objects.get_or_create(id=attendee_data['id']) 
                else:
                    attendee, created = Facilitator.objects.get_or_create(id=attendee_data['id'])

                event.attendees.add(attendee) 

            # add questions to the event
            for question_data in questions_data:
                # check if the question already exists
                question_id = question_data.get('id')
                if question_id:
                    question, created = Question.objects.get_or_create(id=question_data['id']) 
                else: 
                    question = Question.objects.create(**question_data)
                    
                event.questions.add(question) 

            # bulk add attendees & questions to the event to minimize db hits
            if attendees_to_add:
                event.attendees.add(*attendees_to_add)

            if questions_to_add:
                event.questions.add(*questions_to_add)
            
            return event
    
    return EventSerializer


### CUSTOM VIEWSET FUNCTIONS ###

def event_attendee_create_viewset():
    class EventAttendeeViewSet(viewsets.ModelViewSet):
        queryset = Event.objects.all()
        serializer_class = event_attendee_create_serializer()

    return EventAttendeeViewSet


def event_create_viewset(serializers_dict):
    class EventViewSet(viewsets.ModelViewSet):
        queryset = Event.objects.all()
        serializer_class = event_create_serializer(serializers_dict)

    return EventViewSet


### DYNAMICALLY GENERATE SERIALIZERS ###

def generate_serializers():
    serializers_dict = {}

    for app_label, model_name in MODELS_LIST:
        model = get_model(app_label, model_name)
        
        # check for custom serializer
        if model_name in CUSTOM_SERIALIZER_MODELS:
            serializers_dict[(app_label, model_name)] = use_custom_serializer(model_name, serializers_dict)
            continue

        # create Meta class dynamically
        meta_class = type(
            # model name
            'Meta',
            # tuple containing base class (comma ensures treated as a tuple)
            (object,),
            # dictionary defining class attributes
            {
                'model': model,
                'fields': '__all__'
            }
        )

        # create serializer class dynamically
        serializer_class = type(
            f"{model_name}Serializer", 
            (serializers.ModelSerializer,), 
            {
                'Meta': meta_class
            }
            )
        serializers_dict[(app_label, model_name)] = serializer_class
    
    return serializers_dict


### DYNAMICALLY GENERATE VIEWSETS ###
def generate_viewsets(serializers_dict):
    viewsets_dict = {}

    for (app_label, model_name), serializer_class in serializers_dict.items():
        model = get_model(app_label, model_name)

        # check for custom serializer:
        if model_name in CUSTOM_SERIALIZER_MODELS:
            viewset_class = use_custom_viewset(model_name, serializers_dict)
        else:
            viewset_class = type(
                f"{model_name}ViewSet", 
                (viewsets.ModelViewSet,), 
                {
                    'queryset': model.objects.all(),
                    'serializer_class': serializer_class
                })

        viewsets_dict[model_name] = viewset_class

    return viewsets_dict


# generate serializers and viewsets
serializers_dict = generate_serializers()
viewsets_dict = generate_viewsets(serializers_dict)
        

