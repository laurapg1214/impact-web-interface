from django.contrib.auth.models import User
from django.db import models


def get_default_event():
    default_event = Event.objects.first()
    return default_event.id if default_event else None


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


class OrganizationCoordinator(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ManyToManyField("Organization", related_name="coordinators")
    organization_role = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - Coordinator of {self.organization.name}"


class Organization(BaseModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    events = models.ManyToManyField("Event", related_name="organizations", blank=True)

    def __str__(self):
        return f"{self.name} ({self.location})"


class Event(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=50, blank=True)
    # many to many class relationships 
    # placed in Event to manage data primarily from perspective of event entities
    facilitators = models.ManyToManyField("Facilitator", related_name="events", blank=True)
    participants = models.ManyToManyField("Participant", related_name="events", blank=True)
    questions = models.ManyToManyField("Question", related_name="events", blank=True)

    def __str__(self):
        return self.name


class Facilitator(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    
class Participant(BaseModel):
    participant_identifier = models.CharField(max_length=50)  # can be text or emoji

    def __str__(self):
        return self.participant_identifier


class Question(BaseModel):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text
    

class Response(BaseModel):
    text = models.TextField()
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="responses")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="responses", null=True, default=get_default_event)

    def __str__(self):
        return f"Response to '{self.question.text}': {self.text}"



