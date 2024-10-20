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
    organizations = models.ManyToManyField(
        Organization, 
        related_name="events" 
    )
    questions = models.ManyToManyField(
        Question, 
        blank=True,
        related_name="events" 
    )
    
    def __str__(self):
        return f"{self.name}, {self.date}" 
    
    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
    



