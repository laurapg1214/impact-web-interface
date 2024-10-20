from apps.common.models import BaseModel
from apps.events.models import Event
from apps.organizations.models import Organization
from django.db import models

# store demographic categories with field type choices
class DemographicCategory(BaseModel):
    FIELD_TYPE_CHOICES = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('choice', 'Choice'),
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="demographic_categories")
    name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=10, choices=FIELD_TYPE_CHOICES)

    def __str__(self):
        return self.name

# link demographic categories with events
class EventDemographic(BaseModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_demographics")
    category = models.ForeignKey(DemographicCategory, on_delete=models.CASCADE, related_name="event_demographics")
    
    def __str__(self):
        return f"{self.category} for {self.event}"

# store demographic responses from facilitators and participants
class Demographics(BaseModel):
    event_demographic = models.ForeignKey(EventDemographic, on_delete=models.CASCADE, related_name="demographic_responses")
    facilitator = models.ForeignKey('attendees.Facilitator', on_delete=models.CASCADE, null=True, blank=True)
    participant = models.ForeignKey('attendees.Participant', on_delete=models.CASCADE, null=True, blank=True)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"Response for {self.event_demographic.category} by {self.facilitator or self.participant}"
