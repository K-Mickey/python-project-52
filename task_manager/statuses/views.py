from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import AuthRequiredMixin, BoundProtectionMixin
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class StatusListView(AuthRequiredMixin, ListView):
    template_name = "status_list.html"
    model = Status
    context_object_name = "statuses"
    extra_context = {
        "page_title": gettext_lazy("Statuses"),
    }


class StatusCreateView(
    AuthRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    template_name = "form.html"
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy("status_list")
    success_message = gettext_lazy("Status created successfully")
    extra_context = {
        "page_title": gettext_lazy("Create status"),
        "title": gettext_lazy("Create status"),
        "button_text": gettext_lazy("Create"),
    }


class StatusUpdateView(
    AuthRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    template_name = "form.html"
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy("status_list")
    success_message = gettext_lazy("Status updated successfully")
    extra_context = {
        "page_title": gettext_lazy("Update status"),
        "title": gettext_lazy("Update status"),
        "button_text": gettext_lazy("Update"),
    }


class StatusDeleteView(
    AuthRequiredMixin,
    BoundProtectionMixin,
    SuccessMessageMixin,
    DeleteView,
):
    template_name = "delete.html"
    model = Status
    success_url = reverse_lazy("status_list")
    success_message = gettext_lazy("Status deleted successfully")
    protected_url = reverse_lazy("status_list")
    protected_message = gettext_lazy("Unable to delete status")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = gettext_lazy("Delete status")
        context["title"] = gettext_lazy("Delete status")
        context["deleting_object"] = self.object.name
        return context
