from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from task_manager.users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
    )
    search_fields = (
        "username",
        "first_name",
        "last_name",
    )
