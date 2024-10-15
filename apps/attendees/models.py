from apps.common.models import BaseModel
from apps.events.models import Event
from apps.organizations.models import Organization
from django.db import models
import uuid


### CONTAINS Facilitator, Participant, EventParticipant, Demographics, CustomDemographicField, CustomDemographicValue ###

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
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_participants")
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="participant_events")

    class Meta:
        verbose_name = "Event Participant"
        verbose_name_plural = "Event Participants"

    def __str__(self):
        participants = self.event.eventparticipant_set.all()
        participant_info = [
            f"{p.unique_id} {p.first_name} {p.last_name}" for p in participants
        ]
        return f"{self.event.name} participants: {', '.join(participant_info)}"
    

class Demographics(BaseModel):
    GENDER_CHOICES = [
        ('F', 'Female'),
        ('M', 'Male'),
        ('NB', 'Non-binary'),
        ('O', 'Other'),
        ('U', 'Prefer not to say'),
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="demographics")
    events = models.ManyToManyField(Event, related_name="demographics")
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    # TODO: need ETHNICITY_CHOICES (customizable)
    ethnicity = models.CharField(max_length=100, blank=True) 
    location = models.CharField(max_length=255, blank=True)

    # foreign keys
    facilitator = models.OneToOneField(Facilitator, on_delete=models.CASCADE, blank=True, null=True)
    participant = models.OneToOneField(Participant, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Demographics for {self.facilitator or self.participant}"
    

# create custom demographic field
class CustomDemographicField(BaseModel):
    FIELD_TYPE_CHOICES = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('choice', 'Choice'),
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="custom_demographic_fields")
    events = models.ManyToManyField(Event, related_name="custom_demographic_fields")
    name = models.Charfield(max_length=100)
    field_type = models.CharField(max_length=10, choices=FIELD_TYPE_CHOICES)
    choices = models.TextField(blank=True, help_text="Comma-separated values for choice fields (if applicable)")
    required = models.BooleanField(default=False)

    def __str__(self):
        return f"Custom Field: {self.name} ({self.get_field_type_display()})"
    

# store custom field values
class CustomDemographicValue(BaseModel):
    demographic = models.ForeignKey(Demographics, on_delete=models.CASCADE, related_name="custom_values")
    field = models.ForeignKey(CustomDemographicField, on_delete=models.CASCADE)
    value = models.Charfield(max_length=255)

    def __str__(self):
        return f"Value for {self.field.name}: {self.value}"