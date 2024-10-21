from apps.common.models import BaseModel, AttendeeInfoModel
from apps.common.utils import get_default_event
from apps.organizations.models import Organization
from django.core.exceptions import ValidationError
from django.db import models
import uuid


### CONTAINS Participant, Facilitator, CustomAttendeeType, EventAttendee ###
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

    def __str__(self):
        return f"{self.unique_id} {self.first_name} {self.last_name} - Participant"

    class Meta:
        verbose_name = "Participant"
        verbose_name_plural = "Participants"


class Facilitator(BaseModel, AttendeeInfoModel):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="facilitators"
    )
    organization_role = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return (
            f"{self.first_name} {self.last_name} - "
            "Facilitator for {self.organization.name}"
        )
    
    class Meta:
        verbose_name = "Facilitator"
        verbose_name_plural = "Facilitators"


# allow coordinators to create custom attendees for one-off events or longterm use
class CustomAttendeeType(BaseModel, AttendeeInfoModel):
    type_name = models.CharField(max_length=50, unique=True)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="custom_attendee_types"
    )
    organization_role = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.type_name
    
    class Meta:
        verbose_name = "Custom Attendee Type"
        verbose_name_plural = "Custom Attendee Types"


class EventAttendee(BaseModel):
    
    EVENT_ATTENDEE_TYPES = [
        ("participant", "Participant"),
        ("facilitator", "Facilitator"),
        ("other", "Other"), # custom types
    ]

    ### VALIDATION CHECK ###

    # validation check that facilitator's organization in event's organization(s)
    def clean(self):
        # map attendee types to their specific instances
        attendee_map = {
            "participant": self.participant,
            "facilitator": self.facilitator,
            "other": self.custom_attendee_type,
        }

        # get current attendee instance based on type
        attendee_instance = attendee_map.get(self.attendee_type)

        # conditional validation check if attendee instance exists
        if attendee_instance is not None:
            if attendee_instance.organization not in self.event.organizations.all():
                raise ValidationError(
                    f"{self.attendee_type.capitalize()} does not belong to any "
                    "of the organizations running the event"
                )
    
    # run validation on save
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    ### FIELDS ###    

    # PROTECT below for to maintain all events that were run and their attendees
    event = models.ForeignKey(
        # importing via string to avoid circular import
        "events.Event", 
        on_delete=models.PROTECT, 
        default=get_default_event,
        related_name="event_attendees"
    )
    # allows multiple orgs running an event to all have access to EventAttendees
    organizations = models.ManyToManyField(
        Organization,
        related_name = "event_attendees"
    )
    attendee_type = models.CharField(
        max_length=20, 
        choices=EVENT_ATTENDEE_TYPES,
        default="participant"
    )
    participant = models.ForeignKey(
        Participant, 
        null=True,
        blank=True, 
        on_delete=models.PROTECT, 
        related_name="event_attendees",
    )
    facilitator = models.ForeignKey(
        Facilitator, 
        null=True,
        blank=True, 
        on_delete=models.PROTECT,  
        related_name="event_attendees",
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
            ("attended", "Attended"), 
            ("absent", "Absent")
        ], 
        default="attended"
    )

    def __str__(self):
        attendee = self.participant or self.facilitator or self.custom_attendee_type
        return f"{self.attendee_type.capitalize()}: {attendee} at {self.event}"

    class Meta:
        # avoid duplicate registrations: 
        # ensure each attendee assigned to specific event only once
        unique_together = (
            ("event", "participant"),
            ("event", "facilitator"),
            ("event", "custom_attendee_type", "participant"),
            ("event", "custom_attendee_type", "facilitator"),
        )
        verbose_name = "Event Attendee"
        verbose_name_plural = "Event Attendees"
        
    
