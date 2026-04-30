from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, ModelForm
from django.utils.translation import gettext_lazy

from task_manager.users.models import User


class UserForm(UserCreationForm):
    first_name = CharField(required=True, label=gettext_lazy("First name"))
    last_name = CharField(required=True, label=gettext_lazy("Last name"))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        )


class UserUpdateForm(ModelForm):
    first_name = CharField(required=True, label=gettext_lazy("First name"))
    last_name = CharField(required=True, label=gettext_lazy("Last name"))

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
        )
