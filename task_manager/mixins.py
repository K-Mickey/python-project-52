from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect


class AuthRequiredMixin(LoginRequiredMixin):
    auth_message = None
    auth_url = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.auth_message)
            return redirect(self.auth_url)

        return super().dispatch(request, *args, **kwargs)


class UserOwnershipMixin(UserPassesTestMixin):
    ownership_message = None
    ownership_url = None

    def test_func(self):
        return self.request.user == self.get_object()

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.test_func()
        if not user_test_result:
            messages.error(self.request, self.ownership_message)
            return redirect(self.ownership_url)
        return super().dispatch(request, *args, **kwargs)
