from django.db.models import CASCADE, PROTECT, CharField, DateTimeField, ForeignKey, ManyToManyField, Model, TextField
from django.utils.translation import gettext_lazy

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(Model):
    name = CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        verbose_name=gettext_lazy("Name"),
    )
    description = TextField(
        max_length=1000,
        blank=True,
        null=False,
        verbose_name=gettext_lazy("Description"),
    )
    status = ForeignKey(
        Status,
        on_delete=PROTECT,
        related_name="tasks",
        verbose_name=gettext_lazy("Status"),
    )
    author = ForeignKey(
        User,
        on_delete=PROTECT,
        related_name="created_tasks",
        verbose_name=gettext_lazy("Author"),
    )
    executor = ForeignKey(
        User,
        on_delete=PROTECT,
        related_name="tasks",
        verbose_name=gettext_lazy("Executor"),
    )
    labels = ManyToManyField(
        Label,
        through="TaskLabel",
        through_fields=("task", "label"),
        blank=True,
        related_name="tasks",
        verbose_name=gettext_lazy("Labels"),
    )
    date_created = DateTimeField(
        auto_now_add=True,
        verbose_name=gettext_lazy("Creation date"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = gettext_lazy("Task")
        verbose_name_plural = gettext_lazy("Tasks")


class TaskLabel(Model):
    task = ForeignKey(Task, on_delete=CASCADE)
    label = ForeignKey(Label, on_delete=PROTECT)
