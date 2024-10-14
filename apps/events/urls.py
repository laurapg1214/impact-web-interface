from django.urls import path
from .views import EventCreateView

app_name = 'events'

urlpatterns = [
    path('create/', EventCreateView.as_view(), name='event-create'),
]



