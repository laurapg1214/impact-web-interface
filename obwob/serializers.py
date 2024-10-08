from .models import *
from rest_framework import serializers


###  PEOPLE  ###

class OrganizationCoordinatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationCoordinator
        fields = '__all__'


class FacilitatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facilitator
        fields = '__all__'


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'


###  EVENTS/QUESTIONS/RESPONSES  ###

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = '__all__'


###  ORGANIZATION  ###

class OrganizationSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True)


    class Meta:
        model = Organization
        fields = '__all__'

    
    def create(self, validated_data):
        events_data = validated_data.pop('events') # extract event data
        organization = Organization.objects.create(**validated_data) # create the organization
        for event_data in events_data:
            event, created = Event.objects.get_or_create(**event_data) # create or get events
            organization.events.add(event) # add events to the organization
        return organization