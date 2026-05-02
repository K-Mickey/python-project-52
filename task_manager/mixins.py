from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy


class AuthRequiredMixin(LoginRequiredMixin):
    auth_url = reverse_lazy("login")
    auth_message = gettext_lazy("You are not logged in")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.auth_message)
            return redirect(self.auth_url)

        return super().dispatch(request, *args, **kwargs)


class UserOwnershipMixin(UserPassesTestMixin):
    ownership_url = None
    ownership_message = gettext_lazy("You have no rights to change it.")

    def test_func(self):
        return self.request.user == self.get_object()

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.test_func()
        if not user_test_result:
            messages.error(self.request, self.ownership_message)
            return redirect(self.ownership_url)
        return super().dispatch(request, *args, **kwargs)


class ProtectedBoundFieldMixin:
    protected_url = None
    protected_message = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_url)
