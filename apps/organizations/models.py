from apps.common.models import BaseModel
from django.db import models


class Organization(BaseModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"
    
    def __str__(self):
        return f"{self.name} ({self.location})"

