from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class LabelsConfig(AppConfig):
    name = "task_manager.labels"
    verbose_name = gettext_lazy("Labels")
