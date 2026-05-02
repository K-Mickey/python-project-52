from django.utils.translation import gettext_lazy
from django.views.generic import ListView

from task_manager.labels.models import Label
from task_manager.mixins import AuthRequiredMixin


class LabelListView(AuthRequiredMixin, ListView):
    template_name = "label_list.html"
    model = Label
    context_object_name = "labels"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = gettext_lazy("Labels")
        return context
