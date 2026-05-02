from django.forms import CharField, ModelForm
from django.utils.translation import gettext_lazy

from task_manager.tasks.models import Task


class TaskForm(ModelForm):
    name = CharField(
        max_length=150,
        required=True,
        label=gettext_lazy("Name"),
    )

    class Meta:
        model = Task
        fields = (
            "name",
            "description",
            "status",
            "executor",
            "labels",
        )
