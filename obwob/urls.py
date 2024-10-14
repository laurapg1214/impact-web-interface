"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
#from django.conf.urls import handler404
from django.conf.urls.static import static
from rest_framework import routers
from apps.common.utils import viewsets_dict
from apps.events.views import index
#from .views import custom_404_view

app_name = "obwob"

#handler404 = custom_404_view

# URL configurations for API layer using DRF's routers
router = routers.DefaultRouter()

# register each viewset dynamically with the router using custom utils functionality
for model_name, viewset_class in viewsets_dict.items():
    router.register(model_name.lower(), viewset_class, basename=model_name.lower())

urlpatterns = [
    path("admin/", admin.site.urls),
    path("apps/events/", include("apps.events.urls")),

    # api routes
    path('api/', include(router.urls)),

    # static routes
    path('', index, name="index"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

