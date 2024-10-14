from apps.events.models import Event
from apps.attendees.models import Facilitator, Participant
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
    ### ORGANIZATION ###
    'Organization',

    ### PEOPLE ###
    'Coordinator',
    'Facilitator',
    'Participant',
    'EventParticipant',
    
    ### QUESTIONS/EVENTS/RESPONSES ###
    'Question',
    'Event',
    'Response',
    ]


# dynamically import models from specified app
def get_model(app_label, model_name):
    return apps.get_model(app_label, model_name)


### GENERATE CUSTOM SERIALIZERS & VIEWSETS (standard serialization & viewset generation below) ###

CUSTOM_SERIALIZER_MODELS = [
    'EventParticipant',
    'Event',
]

# function to call custom serializers generation within generate serializers & viewsets functions below
# keep updated whenever custom serializer or viewset function added
def use_custom_serializer(model_name, serializers_dict):
    if model_name == 'EventParticipant':
        return event_participant_create_serializer() 
    elif model_name == 'Event':
        return event_create_serializer(serializers_dict)
    
    
def use_custom_viewset(model_name, serializers_dict):
    if model_name == 'EventParticipant':
        return event_participant_create_viewset()
    elif model_name == 'Event':
        return event_create_viewset(serializers_dict)
    

# custom serializer functions 
# dynamically add participants during live event
def event_participant_create_serializer(): 
    class EventParticipantSerializer(serializers.ModelSerializer):
        class Meta:
            model = Event
            fields = ['participants']

        def update(self, instance, validated_data):
            participants_data = validated_data.pop('participants', [])

            # create lists for both existing and new participants, for bulk adding to minimize db hits
            participants_to_create = []
            participants_to_add = []

            for participant_data in participants_data:
                # automatically assign a unique identifier if not provided
                unique_id = participant_data.get('unique_id') or str(uuid.uuid4())
                
                # find or create the participant
                participant, created = Participant.objects.get_or_create(
                    unique_id=unique_id,
                    defaults={
                        'first_name': participant_data.get('first_name', ''),
                        'last_name': participant_data.get('last_name', '')
                    }
                )
                
                if created:
                    participants_to_create.append(participant)
                else:
                    participants_to_add.append(participant)

            # bulk create new participants
            Participant.objects.bulk_create(participants_to_create)

            # add new and existing participants to the event
            if participants_to_create or participants_to_add:
                instance.participants.add(*participants_to_create, *participants_to_add)
            
            return instance
        
    return EventParticipantSerializer
    

def event_create_serializer(serializers_dict):
    class EventSerializer(serializers.ModelSerializer):
        facilitators = serializers_dict.get('Facilitator')(many=True)
        questions = serializers_dict.get('Question')(many=True)

        class Meta:
            model = Event
            fields = '__all__'

        def create(self, validated_data):
            # extract facilitator, participants and questions data if present
            facilitators_data = validated_data.pop('facilitators', []) 
            questions_data = validated_data.pop('questions', [])

            # create the event object
            event = Event.objects.create(**validated_data) 

            # prepare lists for bulk creation
            facilitators_to_add = []
            questions_to_add = []

            # add facilitators to the event
            for facilitator_data in facilitators_data:
                facilitator, created = Facilitator.objects.get_or_create(id=facilitator_data['id']) 
                event.facilitators.add(facilitator) 

            # add questions to the event
            for question_data in questions_data:
                # check if the question already exists
                question_id = question_data.get('id')
                if question_id:
                    question, created = Question.objects.get_or_create(id=question_data['id']) 
                else: 
                    question = Question.objects.create(**question_data)
                    
                event.questions.add(question) 

            # bulk add facilitators & questions to the event to minimize db hits
            if facilitators_to_add:
                event.facilitators.add(*facilitators_to_add)

            if questions_to_add:
                event.questions.add(*questions_to_add)
            
            return event
    
    return EventSerializer


# custom viewset functions
def event_participant_create_viewset():
    class EventParticipantViewSet(viewsets.ModelViewSet):
        queryset = Event.objects.all()
        serializer_class = event_participant_create_serializer()

    return EventParticipantViewSet


def event_create_viewset(serializers_dict):
    class EventViewSet(viewsets.ModelViewSet):
        queryset = Event.objects.all()
        serializer_class = event_create_serializer(serializers_dict)

    return EventViewSet


### DYNAMICALLY GENERATE SERIALIZERS & VIEWSETS FOR EACH MODEL (EXCEPT CUSTOM) ###
def generate_serializers():
    serializers_dict = {}

    for model_name in MODELS_LIST:
        model = get_model(model_name)
        
        # check for custom serializer
        if model_name in CUSTOM_SERIALIZER_MODELS:
            serializers_dict[model_name] = use_custom_serializer(model_name, serializers_dict)
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
        serializers_dict[model_name] = serializer_class
    
    return serializers_dict


# define serializers_dict
serializers_dict = generate_serializers()


# dynamically generate viewsets for each model
def generate_viewsets(serializers_dict):
    viewsets_dict = {}

    for model_name, serializer_class in serializers_dict.items():
        model = get_model(model_name)

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


# define viewsets_dict
viewsets_dict = generate_viewsets(serializers_dict)
        

