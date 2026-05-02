from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from task_manager.mixins import AuthorProtectionMixin, AuthRequiredMixin
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskForm
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


class TaskCreateView(
    AuthRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    template_name = "form.html"
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_list")
    success_message = gettext_lazy("Task successfully created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = gettext_lazy("Create task")
        context["title"] = gettext_lazy("Create task")
        context["button_text"] = gettext_lazy("Create")
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(
    AuthRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    template_name = "form.html"
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_list")
    success_message = gettext_lazy("Task successfully updated")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = gettext_lazy("Update task")
        context["title"] = gettext_lazy("Update task")
        context["button_text"] = gettext_lazy("Update")
        return context


class TaskDeleteView(
    AuthRequiredMixin,
    AuthorProtectionMixin,
    SuccessMessageMixin,
    DeleteView,
):
    template_name = "delete.html"
    model = Task
    success_url = reverse_lazy("task_list")
    success_message = gettext_lazy("Task successfully deleted")
    author_field = "author"
    permission_url = reverse_lazy("task_list")
    permission_message = gettext_lazy("The task can be deleted only by its author")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = gettext_lazy("Delete task")
        context["title"] = gettext_lazy("Delete task")
        context["deleting_object"] = self.object.name
        return context


class TaskDetailView(AuthRequiredMixin, DetailView):
    template_name = "task_detail.html"
    model = Task
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.object.name
        return context
