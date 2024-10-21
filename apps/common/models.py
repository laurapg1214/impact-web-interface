from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    # timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # soft delete fields
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # flag record as deleted; keep in db
    def delete_record(self):
        # set the is_deleted flag & deleted_at timestamp
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save() # save the changes instead of deleting

    # restore soft deleted records
    def restore(self):
        # remove the is_deleted flag & deleted_at timestamp
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    # override default delete method to prevent hard deletes
    def delete(self, *args, **kwargs):
        raise NotImplementedError(
            "Use delete_record() to perform a soft delete "
            "and keep the record in the database."
        )
    
    # filter soft deleted records
    # TODO: work out querying with relationships
    @classmethod
    def active_records(cls):
        return cls.objects.filter(is_deleted=False)

    def __str__(self):
        # return generic message as default
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
    # TODO from phonenumber_field.modelfields import PhoneNumberField
    phone_number = models.CharField(max_length=50, null=True, blank=True)

    class CustomFieldValue(models.Model):
        CUSTOM_FIELD_TYPES = [
            ("text", "Text"),
            ("number", "Number"),
            ("date", "Date"),
            # for choice options, see class CustomFieldChoice below
            ("choice", "Choice"),
        ]

        attendee = models.ForeignKey(
            # string ref to avoid circular imports as defined w/in same class
            "AttendeeInfoModel",
            on_delete=models.CASCADE,
            related_name="custom_field_values"
        )
        field_name = models.CharField(max_length=100)
        field_type = models.CharField(max_length=10, choices=CUSTOM_FIELD_TYPES)
        value=models.TextField()

        class Meta:
            abstract = True
            unique_together = ("attendee", "field_name")

    # allows coordinators to provide choices in custom fields
    class CustomFieldChoice(models.Model):
        # allow multiple choice options
        custom_field_value = models.ForeignKey(
            "CustomFieldValue",
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
            unique_together = ("custom_field_value", "choice_text")

    class Meta:
        abstract = True  

