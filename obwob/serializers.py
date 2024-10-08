from .models import *
from rest_framework import serializers
import uuid


###  ORGANIZATION  ###

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


###  PEOPLE  ###

class OrganizationCoordinatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationCoordinator
        fields = '__all__'


class FacilitatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facilitator
        fields = '__all__'


class EventParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['participants']

   # add participants dynamically while event is live without modifying EventSerializer 
    def update(self, instance, validated_data):
        participants_data = validated_data.pop('participants', [])
        for participant_data in participants_data:
            # automatically assign a unique identifier if not provided
            participant_identifier = participant_data.get('participant_identifier') or str(uuid.uuid4())
            
            # find or create the participant
            participant, created = Participant.objects.get_or_create(
                participant_identifier=participant_identifier,
                defaults={
                    'first_name': participant_data.get('first_name', ''),
                    'last_name': participant_data.get('last_name', '')
                }
            )
            # add participant to the event
            instance.participants.add(participant)
        return instance


###  QUESTIONS/EVENTS/RESPONSES  ###

class EventSerializer(serializers.ModelSerializer):
    facilitators = FacilitatorSerializer(many=True)
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        # extract facilitator, participants and questions data if present
        facilitators_data = validated_data.pop('facilitators', []) 
        questions_data = validated_data.pop('questions', [])

        # create the event object
        event = Event.objects.create(**validated_data) 

        # add facilitators to the event
        for facilitator_data in facilitators_data:
            facilitator, created = Facilitator.objects.get_or_create(id=facilitator_data['id']) 
            event.facilitators.add(facilitator) 

        # add questions to the event
        for question_data in questions_data:
            question, created = Question.objects.get_or_create(id=question_data['id']) 
            event.questions.add(question) 

        return event
    

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = '__all__'



