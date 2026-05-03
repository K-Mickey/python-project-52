from django.forms import CheckboxInput
from django.utils.translation import gettext_lazy
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter

from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class TaskFilter(FilterSet):
    labels = ModelChoiceFilter(
        label=gettext_lazy("Label"),
        queryset=Label.objects.all(),
    )
    own_tasks = BooleanFilter(
        label=gettext_lazy("Only own tasks"),
        method="filter_own_tasks",
        widget=CheckboxInput,
    )

    def filter_own_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ["status", "executor"]
