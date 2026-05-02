from django.contrib import admin
from django.utils.translation import gettext_lazy

from task_manager.tasks.models import Task, TaskLabel


class TaskLabelInline(admin.TabularInline):
    model = TaskLabel
    extra = 1
    verbose_name = gettext_lazy("Label")
    verbose_name_plural = gettext_lazy("Labels")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [TaskLabelInline]

    list_display = ("name", "status", "author", "executor", "date_created")
    list_filter = ("status", "author", "executor")
    search_fields = ("name", "description")
    autocomplete_fields = ("author", "executor", "status", "labels")
