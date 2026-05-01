from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class StatusListView(ListView):
    template_name = "statuses/status_list.html"
    model = Status
    context_object_name = "statuses"
    extra_context = {
        "page_title": gettext_lazy("Statuses"),
    }


class StatusCreateView(CreateView):
    template_name = "form.html"
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy("status_list")
    extra_context = {
        "page_title": gettext_lazy("Create status"),
        "title": gettext_lazy("Create status"),
        "button_text": gettext_lazy("Create"),
    }


class StatusUpdateView(UpdateView):
    template_name = "form.html"
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy("status_list")
    extra_context = {
        "page_title": gettext_lazy("Update status"),
        "title": gettext_lazy("Update status"),
        "button_text": gettext_lazy("Update"),
    }


class StatusDeleteView(DeleteView):
    template_name = "statuses/delete.html"
    model = Status
    success_url = reverse_lazy("status_list")
    extra_context = {
        "page_title": gettext_lazy("Delete status"),
    }
