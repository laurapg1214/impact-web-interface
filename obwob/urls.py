from . import views
from django.conf import settings
#from django.conf.urls import handler404
from django.conf.urls.static import static
from django.urls import path
#from .views import custom_404_view

app_name = "obwob"
urlpatterns = [
    path("", views.index, name="index"),
    # event view
    path("<int:event_id>_<event_name>", views.event, name="event"),
    # event questions (all)
    path("<int:event_id>_<event_name>/questions", views.event_questions, name="event_questions"),
    # individual question prompt
    path("<int:event_id>_<event_name>/<int:question_id>_question", views.prompt, name="prompt"),
    # question responses (all)
    path("<int:question_id>_question/responses", views.responses, name="responses"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

#handler404 = custom_404_view