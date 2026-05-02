from django.utils.translation import gettext_lazy
from django_filters import FilterSet, ModelMultipleChoiceFilter

from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class TaskFilter(FilterSet):
    labels = ModelMultipleChoiceFilter(
        label=gettext_lazy("Labels"),
        queryset=Label.objects.all(),
        method="filter_labels",
    )

    @staticmethod
    def filter_labels(queryset, name, value):
        if value:
            return queryset.filter(labels__in=value).distinct()
        return queryset

    class Meta:
        model = Task
        fields = ["status", "author", "executor"]
