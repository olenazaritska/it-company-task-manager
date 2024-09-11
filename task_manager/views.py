from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import TaskForm, WorkerCreationForm, WorkerUpdateForm
from task_manager.models import Worker, Task


@login_required
def index(request):
    return render(request, "task_manager/index.html")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    queryset = Worker.objects.select_related("position")
    paginate_by = 4


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.object
        context["completed_tasks_count"] = (
            worker.tasks.filter(is_completed=True).count()
        )
        context["pending_tasks_count"] = (
            worker.tasks.filter(is_completed=False).count()
        )

        pending_tasks = worker.tasks.filter(is_completed=False)
        for task in pending_tasks:
            task.other_assignees = task.assignees.exclude(id=worker.id)
        context["pending_tasks"] = pending_tasks

        return context


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("task-manager:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm

    def get_success_url(self):
        return reverse_lazy(
            "task-manager:worker-detail",
            kwargs={"pk": self.object.pk}
        )

    def dispatch(self, request, *args, **kwargs):
        worker = self.get_object()
        if worker.id != request.user.id:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task-manager:worker-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    queryset = Task.objects.select_related("task_type")

    def get_queryset(self):
        queryset = super().get_queryset()
        completed_filter = self.request.GET.get("completed")
        if completed_filter == "true":
            queryset = queryset.filter(is_completed=True)
        elif completed_filter == "false":
            queryset = queryset.filter(is_completed=False)
        return queryset


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task-manager:task-list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields.pop("is_completed")
        return form


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task-manager:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task-manager:task-list")
