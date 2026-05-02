from django.db.models import CharField, DateTimeField, Model
from django.utils.translation import gettext_lazy


class Label(Model):
    name = CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        verbose_name=gettext_lazy("Name"),
    )
    date_created = DateTimeField(
        auto_now_add=True,
        verbose_name=gettext_lazy("Creation date"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = gettext_lazy("Label")
        verbose_name_plural = gettext_lazy("Labels")
