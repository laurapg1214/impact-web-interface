from apps.common.models import BaseModel
from apps.organizations.models import Organization
from django.contrib.auth.models import User
from django.db import models


class Coordinator(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organizations = models.ManyToManyField(Organization, related_name="coordinators", blank=True)
    organization_role = models.CharField(max_length=100, default="OBWOB Coordinator")

    class Meta:
        verbose_name = "Coordinator"
        verbose_name_plural = "Coordinators"
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - Coordinator of {self.organization.name}"


