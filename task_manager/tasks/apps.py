from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class TasksConfig(AppConfig):
    name = "task_manager.tasks"
    verbose_name = gettext_lazy("Tasks")
