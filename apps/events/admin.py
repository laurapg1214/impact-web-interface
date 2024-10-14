from django.contrib import admin
from .models import Event
from apps.attendees.models import Participant
from apps.questions.models import Question

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    readonly_fields = ('created_at', 'last_modified')

class ParticipantAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'last_modified')

class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'last_modified')

admin.site.register(Event, EventAdmin)

admin.site.register(Participant, ParticipantAdmin)

admin.site.register(Question, QuestionAdmin)

