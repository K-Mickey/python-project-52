from django.utils.translation import gettext_lazy
from django_filters.views import FilterView

from task_manager.mixins import AuthRequiredMixin
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.models import Task


class TaskListView(AuthRequiredMixin, FilterView):
    template_name = "task_list.html"
    model = Task
    filterset_class = TaskFilter
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = gettext_lazy("Tasks")
        return context
