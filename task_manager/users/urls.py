from django.urls import path

from task_manager.users.views import UserListView

urlpatterns = [
    path("", UserListView.as_view(), name="users"),
]