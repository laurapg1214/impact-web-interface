from django.apps import AppConfig


class BaseModelConfig(AppConfig):
    # for autoincrementing id field
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.common"

    # startup logic that requires access to models
    def ready(self):
        from .utils import generate_serializers, generate_viewsets
        self.serializers_dict = generate_serializers()
        self.viewsets_dict = generate_viewsets(self.serializers_dict)