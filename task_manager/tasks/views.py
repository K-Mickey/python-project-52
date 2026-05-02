from django.utils.translation import gettext_lazy
from django.views.generic import ListView

from task_manager.mixins import AuthRequiredMixin
from task_manager.tasks.models import Task


class TaskListView(AuthRequiredMixin, ListView):
    template_name = "task_list.html"
    model = Task
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = gettext_lazy("Tasks")
        return context
