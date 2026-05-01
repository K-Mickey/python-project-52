from django.forms import CharField, ModelForm
from django.utils.translation import gettext_lazy

from task_manager.statuses.models import Status


class StatusForm(ModelForm):
    name = CharField(
        max_length=100,
        required=True,
        label=gettext_lazy("Name"),
    )

    class Meta:
        model = Status
        fields = ("name",)
