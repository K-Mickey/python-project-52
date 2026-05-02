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


class AuthorProtectionMixin(UserPassesTestMixin):
    author_field = None
    permission_url = None
    permission_message = gettext_lazy("You have no rights to change it.")

    def test_func(self):
        request_user = self.request.user
        obj = self.get_object()
        if self.author_field:
            return getattr(obj, self.author_field) == request_user
        return request_user == obj

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.test_func()
        if not user_test_result:
            messages.error(self.request, self.permission_message)
            return redirect(self.permission_url)
        return super().dispatch(request, *args, **kwargs)


class BoundProtectionMixin:
    protected_url = None
    protected_message = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_url)
