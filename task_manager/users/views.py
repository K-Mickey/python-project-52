from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.users.forms import UserForm
from task_manager.users.models import User


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = "form.html"
    form_class = AuthenticationForm
    next_page = reverse_lazy("index")
    success_message = gettext_lazy("You are logged in")
    extra_context = {
        "page_title": gettext_lazy("Log In"),
        "title": gettext_lazy("Log In"),
        "button_text": gettext_lazy("Enter"),
    }


class UserLogoutView(SuccessMessageMixin, LogoutView):
    next_page = reverse_lazy("index")
    success_message = gettext_lazy("You are logged out")


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
    success_message = gettext_lazy("User successfully registered")
    extra_context = {
        "page_title": gettext_lazy("Sign Up"),
        "title": gettext_lazy("Sign Up"),
        "button_text": gettext_lazy("Sign Up"),
    }


class UserUpdateView(
    SuccessMessageMixin,
    UpdateView,
):
    template_name = "form.html"
    model = User
    form_class = UserForm
    success_url = reverse_lazy("user_list")
    success_message = gettext_lazy("User successfully updated")
    extra_context = {
        "page_title": gettext_lazy("Update user"),
        "title": gettext_lazy("Update user"),
        "button_text": gettext_lazy("Update"),
    }


class UserDeleteView(
    SuccessMessageMixin,
    DeleteView,
):
    template_name = "users/delete.html"
    model = User
    success_url = reverse_lazy("user_list")
    success_message = gettext_lazy("User successfully deleted")
    extra_context = {
        "page_title": gettext_lazy("Delete user"),
    }
