from apps.common.models import BaseModel
from apps.organizations.models import Organization
from django.db import models


# models for two types of event attendees: Facilitators and Participants
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