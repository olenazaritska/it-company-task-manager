from django.urls import path

from task_manager.views import (
    index,
    WorkerListView,
    WorkerDetailView
)

urlpatterns = [
    path("", index, name="index"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
]

app_name = "task-manager"
