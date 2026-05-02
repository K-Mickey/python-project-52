from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import AuthorProtectionMixin, AuthRequiredMixin, BoundProtectionMixin
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
    AuthorProtectionMixin,
    SuccessMessageMixin,
    UpdateView,
):
    template_name = "form.html"
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy("user_list")
    success_message = gettext_lazy("User successfully updated")
    permission_url = reverse_lazy("user_list")
    extra_context = {
        "page_title": gettext_lazy("Update user"),
        "title": gettext_lazy("Update user"),
        "button_text": gettext_lazy("Update"),
    }


class UserDeleteView(
    AuthRequiredMixin,
    AuthorProtectionMixin,
    BoundProtectionMixin,
    SuccessMessageMixin,
    DeleteView,
):
    template_name = "delete.html"
    model = User
    success_url = reverse_lazy("user_list")
    success_message = gettext_lazy("User successfully deleted")
    protected_url = reverse_lazy("user_list")
    protected_message = gettext_lazy("Unable to delete user")
    permission_url = reverse_lazy("user_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = gettext_lazy("Delete user")
        context["title"] = gettext_lazy("Delete user")
        context["deleting_object"] = self.object.get_full_name()
        return context
