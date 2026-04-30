from django.urls import path

from task_manager.users.views import UserCreateView, UserListView

urlpatterns = [
    path("", UserListView.as_view(), name="users"),
    path("create/", UserCreateView.as_view(), name="sign_up"),
]
