from apps.common.models import BaseModel
from apps.organizations.models import Organization
from apps.questions.models import Question
from django.db import models
  

class Event(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=50, blank=True)
    # manytomany rels placed in Event to manage data primarily from perspective of events
    organizations = models.ManyToManyField(Organization, related_name="events", blank=True)
    questions = models.ManyToManyField(Question, related_name="events", blank=True)

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
    
    def __str__(self):
        return f"{self.name}, {self.date}" 
    



