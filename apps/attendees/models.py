from apps.common.models import BaseModel, AttendeeInfoModel
from apps.organizations.models import Organization
from django.core.exceptions import ValidationError
from django.db import models
import uuid

### CONTAINS Participant, Facilitator, CustomAttendeeType, EventAttendee ###
# Facilitators can belong to only one organization
# Participants & CustomAttendeeTypes can belong to more than one organization

class Participant(BaseModel, AttendeeInfoModel):
    emoji = models.CharField(max_length=10, null=True, blank=True)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="participants"
    )

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


class Facilitator(BaseModel, AttendeeInfoModel):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="facilitators"
    )
    organization_role = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Facilitator"
        verbose_name_plural = "Facilitators"
    
    def __str__(self):
        return (
            f"{self.first_name} {self.last_name} - "
            "Facilitator for {self.organization.name}"
        )


# allow coordinators to create custom attendees for one-off events or longterm use
class CustomAttendeeType(BaseModel, AttendeeInfoModel):
    type_name = models.Charfield(max_length=50, unique=True)

    class Meta:
        verbose_name = "Custom Attendee Type"
        verbose_name_plural = "Custom Attendee Types"

    def __str__(self):
        return self.type_name


class EventAttendee(BaseModel):
    
    EVENT_ATTENDEE_TYPES = [
        ('facilitator', 'Facilitator'),
        ('participant', 'Participant'),
        ('other', 'Other'),
    ]

    ### VALIDATION CHECK ###

    # validation check that facilitator's organization in event's organization(s)
    def clean(self):
        if (
            self.facilitator 
            and self.facilitator.organization 
            not in self.event.organizations.all()
        ):
            raise ValidationError(
                "Facilitator does not belong to any of the organizations running the event"
            )
    
    # run validation on save
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    ### FIELDS ###    

    # PROTECT below for to maintain all events that were run and their attendees
    event = models.ForeignKey(
        # importing via string 'events.Event' 
        # to avoid circular import with events/models.py
        'events.Event', 
        on_delete=models.PROTECT, 
        related_name="attendees"
    )
    # allows multiple orgs running an event to all have access to EventAttendees
    organizations = models.ManyToManyField(
        Organization,
        related_name = 'event_attendees'
    )
    attendee_type = models.CharField(
        max_length=20, 
        choices=EVENT_ATTENDEE_TYPES,
        default='participant'
    )
    participant = models.ForeignKey(
        Participant, 
        null=True,
        blank=True, 
        on_delete=models.PROTECT, 
        related_name="event_participants",
    )
    facilitator = models.ForeignKey(
        Facilitator, 
        null=True,
        blank=True, 
        on_delete=models.PROTECT,  
        related_name="event_facilitators",
    )
    custom_attendee_type = models.ForeignKey(
        CustomAttendeeType,
        null=True,
        blank=True, 
        on_delete=models.PROTECT, 
        related_name="event_attendees",
    )
    registration_time = models.DateTimeField(auto_now_add=True)
    attendance_status = models.CharField(
        max_length=20, 
        choices=[
            ('attended', 'Attended'), 
            ('absent', 'Absent')
        ], 
        default='attended'
    )

    class Meta:
        # avoid duplicate registrations: 
        # ensure each attendee assigned to specific event only once
        unique_together = (
            ('event', 'participant'),
            ('event', 'facilitator'),
            ('event', 'custom_attendee_type', 'participant')
            ('event', 'custom_attendee_type', 'facilitator'),
        )
        verbose_name = "Event Attendee"
        verbose_name_plural = "Event Attendees"

    def __str__(self):
        attendee = self.participant or self.facilitator or self.custom_attendee_type
        return f"{self.attendee_type.capitalize()}: {attendee} at {self.event}"
        
    
