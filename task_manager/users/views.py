from django.utils.translation import gettext_lazy
from django.views.generic import ListView

from task_manager.users.models import User


class UserListView(ListView):
    template_name = "users/users.html"
    model = User
    context_object_name = "users"
    extra_context = {"page_title": gettext_lazy("Users")}
