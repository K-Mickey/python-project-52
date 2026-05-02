# Register your models here.
from django.contrib import admin

from task_manager.statuses.models import Status


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("name", "date_created")
    search_fields = ("name",)
    list_filter = ("date_created",)
