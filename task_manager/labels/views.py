from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.mixins import AuthRequiredMixin, BoundProtectionMixin


class LabelListView(AuthRequiredMixin, ListView):
    template_name = "label_list.html"
    model = Label
    context_object_name = "labels"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = gettext_lazy("Labels")
        return context


class LabelCreateView(
    AuthRequiredMixin,
    CreateView,
):
    template_name = "form.html"
    model = Label
    form_class = LabelForm
    success_url = reverse_lazy("label_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = gettext_lazy("Create label")
        context["title"] = gettext_lazy("Create label")
        context["button_text"] = gettext_lazy("Create")
        return context


class LabelUpdateView(
    AuthRequiredMixin,
    UpdateView,
):
    template_name = "form.html"
    model = Label
    form_class = LabelForm
    success_url = reverse_lazy("label_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = gettext_lazy("Update label")
        context["title"] = gettext_lazy("Update label")
        context["button_text"] = gettext_lazy("Update")
        return context


class LabelDeleteView(
    AuthRequiredMixin,
    BoundProtectionMixin,
    DeleteView,
):
    template_name = "delete.html"
    model = Label
    success_url = reverse_lazy("label_list")
    protected_url = reverse_lazy("label_list")
    protected_message = gettext_lazy("Unable to delete label")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = gettext_lazy("Delete label")
        context["title"] = gettext_lazy("Delete label")
        context["deleting_object"] = self.object.name
        return context
