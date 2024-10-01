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


class Event(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=50, blank=True)
    # many to many class relationships 
    # placed in Event to manage data primarily from perspective of event entities
    participants = models.ManyToManyField("Participant", related_name="events", blank=True)
    questions = models.ManyToManyField("Question", related_name="events", blank=True)

    def __str__(self):
        return self.name
    
    
class Participant(BaseModel):
    participant_identifier = models.CharField(max_length=50)  # can be text or emoji

    def __str__(self):
        return self.participant_identifier


class Question(BaseModel):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text
    

class Response(BaseModel):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="responses")
    text = models.TextField()

    def __str__(self):
        return f"Response to '{self.question.text}': {self.text}"



