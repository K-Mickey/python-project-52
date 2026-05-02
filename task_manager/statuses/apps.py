from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class StatusesConfig(AppConfig):
    name = "task_manager.statuses"
    verbose_name = gettext_lazy("Statuses")
