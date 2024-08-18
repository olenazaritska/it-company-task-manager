from django.urls import path

from task_manager.views import (
    index,
    WorkerListView,
)

urlpatterns = [
    path("", index, name="index"),
]

app_name = "task-manager"
