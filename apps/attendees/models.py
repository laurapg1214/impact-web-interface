from apps.common.models import BaseModel
from apps.organizations.models import Organization
from django.db import models
import uuid


### CONTAINS Facilitator, Participant, EventAttendee ###

class Facilitator(BaseModel):
    unique_id = models.CharField(max_length=50, unique=True, blank=True) # can be chosen by user or automatically assigned
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
    

class EventAttendee(BaseModel):
    EVENT_ATTENDEE_TYPES = [
        'facilitator',
        'participant',
    ]

    # importing via string 'events.Event' to avoid circular import with events/models.py
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name="attendees")
    attendee_type = models.CharField(max_length=20, choices=EVENT_ATTENDEE_TYPES)
    facilitator = models.ForeignKey(Facilitator, on_delete=models.CASCADE, blank=True, null=True, related_name="event_facilitators")
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, blank=True, null=True, related_name="event_participants")
    registration_time = models.DateTimeField(auto_now_add=True)
    attendance_status = models.CharField(max_length=20, choices=[('attended', 'Attended'), ('absent', 'Absent')], default='attended')

    class Meta:
        unique_together = ('event', 'facilitator', 'participant')
        verbose_name = "Event Attendee"
        verbose_name_plural = "Event Attendees"

    def __str__(self):
        return f"{self.attendee_type}: {self.participant or self.facilitator} at {self.event}"
    
