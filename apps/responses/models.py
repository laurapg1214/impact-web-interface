from apps.attendees.models import EventAttendee
from apps.common.models import BaseModel
from apps.questions.models import Question
from django.db import models


class Response(BaseModel):
    text = models.TextField()
    event_attendee = models.ForeignKey(
        EventAttendee, 
        # PROTECT to preserve all submitted responses
        on_delete=models.PROTECT, 
        related_name="responses"
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE, 
        related_name="responses"
    )
    
    def __str__(self):
        return f"Response to '{self.question.text}': {self.text}"
    
    class Meta:
        verbose_name = "Response"
        verbose_name_plural = "Responses"
