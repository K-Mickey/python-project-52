from django.forms import ModelForm
from django.forms.fields import CharField
from django.utils.translation import gettext_lazy

from task_manager.labels.models import Label


class LabelForm(ModelForm):
    name = CharField(
        max_length=100,
        required=True,
        label=gettext_lazy("Name"),
    )

    class Meta:
        model = Label
        fields = ("name",)
