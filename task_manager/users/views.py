from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import AuthRequiredMixin, UserOwnershipMixin
from task_manager.users.forms import UserForm, UserUpdateForm
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


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("index")
    success_message = gettext_lazy("You are logged out")

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super().dispatch(request, *args, **kwargs)


class UserListView(ListView):
    template_name = "user_list.html"
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
    AuthRequiredMixin,
    UserOwnershipMixin,
    SuccessMessageMixin,
    UpdateView,
):
    template_name = "form.html"
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy("user_list")
    success_message = gettext_lazy("User successfully updated")
    ownership_url = reverse_lazy("user_list")
    extra_context = {
        "page_title": gettext_lazy("Update user"),
        "title": gettext_lazy("Update user"),
        "button_text": gettext_lazy("Update"),
    }


class UserDeleteView(
    AuthRequiredMixin,
    UserOwnershipMixin,
    SuccessMessageMixin,
    DeleteView,
):
    template_name = "delete.html"
    model = User
    success_url = reverse_lazy("user_list")
    success_message = gettext_lazy("User successfully deleted")
    ownership_url = reverse_lazy("user_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = gettext_lazy("Delete user")
        context["title"] = gettext_lazy("Delete user")
        context["deleting_object"] = self.object.get_full_name()
        return context

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, gettext_lazy("Unable to delete user because he is being used"))
            return redirect("user_list")
