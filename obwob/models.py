from django.contrib.auth.models import User
from django.db import models
import uuid


###  SETUP  ###

class BaseModel(models.Model):
    # timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        # return generic message
        return f"{self.__class__.__name__} instance"
    
    # make class abstract; won't create db table 
    class Meta:
        abstract = True  


def get_default_event():
    default_event = Event.objects.first()
    return default_event.id if default_event else None


# models below should be kept updated in MODELS_LIST in utils.py
###  ORGANIZATION  ###

class Organization(BaseModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"
    
    def __str__(self):
        return f"{self.name} ({self.location})"

    
###  PEOPLE  ###

class OrganizationCoordinator(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="coordinators", null=True)
    organization_role = models.CharField(max_length=100, default="OBWOB Coordinator")

    class Meta:
        verbose_name = "Organization Coordinator"
        verbose_name_plural = "Organization Coordinators"
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - Coordinator of {self.organization.name}"


class Facilitator(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    organization_role = models.CharField(max_length=100, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="facilitators", null=True)

    class Meta:
        verbose_name = "Facilitator"
        verbose_name_plural = "Facilitators"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - Facilitator for {self.organization.name}"
    
    
class Participant(BaseModel):
    # optional info for participants to enter when joining an event
    unique_id = models.CharField(max_length=50, unique=True, blank=True) # can be chosen by user or automatically assigned
    emoji = models.CharField(max_length=10, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        # if identifier not provided, generate a unique identifier
        if not self.unique_id:
            self.unique_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Participant"
        verbose_name_plural = "Participants"

    def __str__(self):
        return f"{self.unique_id} {self.first_name} {self.last_name} - Participant"
    

class EventParticipant(BaseModel):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name="event_participants")
    participant = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name="participant_events")

    class Meta:
        verbose_name = "Event Participant"
        verbose_name_plural = "Event Participants"

    def __str__(self):
        participants = self.event.eventparticipant_set.all()
        participant_info = [
            f"{p.unique_id} {p.first_name} {p.last_name}" for p in participants
        ]
        return f"{self.event.name} participants: {', '.join(participant_info)}"


###  QUESTIONS/EVENTS/RESPONSES  ###

class Question(BaseModel):
    text = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="questions", null=True)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        
    def __str__(self):
        return self.text
    

class Event(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=50, blank=True)
    # many to many class relationships 
    # placed in Event to manage data primarily from perspective of event entities
    organizations = models.ManyToManyField("Organization", related_name="events", blank=True)
    facilitators = models.ManyToManyField("Facilitator", related_name="events", blank=True)
    participants = models.ManyToManyField("Participant", related_name="events", blank=True)
    questions = models.ManyToManyField("Question", related_name="events", blank=True)

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
    
    def __str__(self):
        return f"{self.name}, {self.date}" 
    

class Response(BaseModel):
    text = models.TextField()
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="responses")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="responses", null=True, default=get_default_event)

    class Meta:
        verbose_name = "Response"
        verbose_name_plural = "Responses"
    
    def __str__(self):
        return f"Response to '{self.question.text}': {self.text}"

