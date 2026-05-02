from django.contrib import admin

from task_manager.labels.models import Label


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ("name", "date_created")
    search_fields = ("name",)
    list_filter = ("date_created",)
