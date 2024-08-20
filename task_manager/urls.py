from django.urls import path

from task_manager.views import (
    index,
    WorkerListView,
    WorkerDetailView,
    WorkerCreateView,
)

urlpatterns = [
    path("", index, name="index"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
]

app_name = "task-manager"
