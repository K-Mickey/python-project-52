from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, ModelForm
from django.forms.widgets import PasswordInput
from django.utils.translation import gettext_lazy

from task_manager.users.models import User


class UserForm(UserCreationForm):
    first_name = CharField(required=True, label=gettext_lazy("First name"))
    last_name = CharField(required=True, label=gettext_lazy("Last name"))

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        )


class UserUpdateForm(ModelForm):
    password = CharField(
        required=False,
        widget=PasswordInput(),
        label=gettext_lazy("Password"),
        help_text=gettext_lazy("Leave blank to keep the same password"),
    )
    password_confirm = CharField(
        required=False,
        widget=PasswordInput(),
        label=gettext_lazy("Password confirmation"),
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
        )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password != password_confirm:
            error = gettext_lazy("The two password fields didn’t match.")
            raise self.add_error("password_confirm", error=error)
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
