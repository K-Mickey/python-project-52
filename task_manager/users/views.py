from django.shortcuts import render
from django.views.generic import ListView

from task_manager.users.models import User


class UserListView(ListView):
    template_name = "users/users.html"
    model = User
    context_object_name = "users"