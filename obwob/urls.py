from . import views
from django.conf import settings
#from django.conf.urls import handler404
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from .utils import viewsets_dict
#from .views import custom_404_view

app_name = "obwob"

# initialize urlpatters
urlpatterns = []

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

#handler404 = custom_404_view

# URL configurations for API layer using DRF's routers
router = routers.DefaultRouter()

# register each viewset dynamically with the router
for model_name, viewset_class in viewsets_dict.items():
    router.register(model_name.lower(), viewset_class, basename=model_name.lower())

urlpatterns = [
    # dynamic routes
    path('api/', include(router.urls)),

    # static routes
    path("", views.index, name="index"),
    # event view
    path("<int:event_id>_<event_name>", views.event, name="event"),
    # event questions (all)
    path("<int:event_id>_<event_name>/questions", views.event_questions, name="event_questions"),
    # question responses (all)
    path("<int:question_id>_question/responses", views.responses, name="responses"),
]

