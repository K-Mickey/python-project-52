from django.db import models
from django.utils.translation import gettext_lazy


class Status(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        verbose_name=gettext_lazy("Name"),
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=gettext_lazy("Date created"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = gettext_lazy("Status")
        verbose_name_plural = gettext_lazy("Statuses")
