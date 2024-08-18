from django.urls import path

from task_manager.views import (
    index,
    WorkerListView,
)

urlpatterns = [
    path("", index, name="index"),
    path("workers/", WorkerListView.as_view(), name="worker-list")
]

app_name = "task-manager"
