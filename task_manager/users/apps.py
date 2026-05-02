from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class UsersConfig(AppConfig):
    name = "task_manager.users"
    verbose_name = gettext_lazy("Users")
