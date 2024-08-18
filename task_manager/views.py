from django.shortcuts import render
from django.views import generic

from task_manager.models import Worker


def index(request):
    return render(request, "task_manager/index.html")


class WorkerListView(generic.ListView):
    model = Worker
    queryset = Worker.objects.select_related("position")
    paginate_by = 4
