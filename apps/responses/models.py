from apps.attendees.models import Facilitator, Participant
from apps.common.models import BaseModel, get_default_event
from apps.events.models import Event
from apps.questions.models import Question
from django.db import models


class Response(BaseModel):
    text = models.TextField()
    facilitator = models.ForeignKey(Facilitator, on_delete=models.CASCADE, related_name="responses")
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(Question,on_delete=models.CASCADE, related_name="responses")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="responses", null=True, default=get_default_event)

    class Meta:
        verbose_name = "Response"
        verbose_name_plural = "Responses"
    
    def __str__(self):
        return f"Response to '{self.question.text}': {self.text}"
