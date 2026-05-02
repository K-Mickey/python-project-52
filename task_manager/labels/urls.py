from django.urls import path

from task_manager.labels.views import LabelListView

urlpatterns = [
    path("", LabelListView.as_view(), name="label_list"),
]
