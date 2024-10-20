from apps.events.models import Event
from apps.organizations.models import Organization
from django.db import models

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


class AttendeeInfoModel(models.Model):
    # unique_id can be chosen by user or automatically assigned
    unique_id = models.CharField(max_length=50, unique=True, blank=True) 
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=254, unique=True, null=True, blank=True)
    phone_number = models.PhoneNumberField(null=True, blank=True)

    CUSTOM_FIELD_TYPES = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        # for choice options, see class CustomFieldChoice below
        ('choice', 'Choice'),
    ]

    class CustomFieldValue(models.Model):
        attendee = models.ForeignKey(
            # string ref to avoid circular imports as defined w/in same class
            'AttendeeInfoModel',
            on_delete=models.CASCADE,
            related_name="custom_field_values"
        )
        field_name = models.CharField(max_length=100)
        field_type = models.CharField(max_length=10, choices=CUSTOM_FIELD_TYPES)
        value=models.TextField()

        class Meta:
            abstract = True
            unique_together = ('attendee', 'field_name')

    # allows coordinators to provide choices in custom fields
    class CustomFieldChoice(model.Models):
        # allow multiple choice options
        custom_field_value = models.ForeignKey(
            'CustomFieldValue',
            on_delete=models.CASCADE,
            related_name="choices"
        )
        choice_text = models.CharField(max_length=100)
        # below: whether choice is currently valid/active; 
        # allows soft deletion without removing from db, and filtering for active
        is_valid = models.BooleanField(default=True)

        class Meta:
            abstract = True
            # ensure choices unique within each custom field
            unique_together = ('custom_field_value', 'choice_text')

    class Meta:
        abstract = True  


def get_default_event():
    default_event = Event.objects.first()
    return default_event.id if default_event else None
