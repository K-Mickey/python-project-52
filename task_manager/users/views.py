from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import CreateView, ListView

from task_manager.users.forms import UserForm
from task_manager.users.models import User


class UserListView(ListView):
    template_name = "users/users.html"
    model = User
    context_object_name = "users"
    extra_context = {"page_title": gettext_lazy("Users")}


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = "form.html"
    model = User
    form_class = UserForm
    success_url = reverse_lazy("login")
    success_message = gettext_lazy("User is successfully registered")
    extra_context = {
        "page_title": gettext_lazy("Sign Up"),
        "title": gettext_lazy("Sign Up"),
        "button_text": gettext_lazy("Sign Up"),
    }
