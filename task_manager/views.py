from django.http import request, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import WorkerForm
from task_manager.models import Worker


def index(request):
    return render(request, "task_manager/index.html")


class WorkerListView(generic.ListView):
    model = Worker
    queryset = Worker.objects.select_related("position")
    paginate_by = 4


class WorkerDetailView(generic.DetailView):
    model = Worker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.object
        context['completed_tasks_count'] = worker.tasks.filter(is_completed=True).count()
        context['pending_tasks_count'] = worker.tasks.filter(is_completed=False).count()

        pending_tasks = worker.tasks.filter(is_completed=False)
        for task in pending_tasks:
            task.other_assignees = task.assignees.exclude(id=worker.id)
        context['pending_tasks'] = pending_tasks

        return context


class WorkerCreateView(generic.CreateView):
    model = Worker
    form_class = WorkerForm
    success_url = reverse_lazy("task-manager:worker-list")


class WorkerUpdateView(generic.UpdateView):
    model = Worker
    form_class = WorkerForm

    def get_success_url(self):
        return reverse_lazy("task-manager:worker-detail", kwargs={"pk": self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        worker = self.get_object()
        if worker.id != request.user.id:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class WorkerDeleteView(generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task-manager:worker-list")
