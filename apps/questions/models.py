from apps.common.models import BaseModel
from apps.organizations.models import Organization
from django.db import models

   
class Question(BaseModel):
    text = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="questions", null=True)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        
    def __str__(self):
        return self.text
    
