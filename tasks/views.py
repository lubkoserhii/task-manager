from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .models import Position, Task, TaskType, Worker
from .searchMixin import SearchMixin


@login_required
def toggle_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_completed = not task.is_completed
    task.save(update_fields=["is_completed"])
    return redirect(request.META.get("HTTP_REFERER", "tasks:task-list"))


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "tasks/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_tasks"] = Task.objects.count()
        context["num_completed_tasks"] = Task.objects.filter(
            is_completed=True
        ).count()
        context["num_workers"] = Worker.objects.count()
        return context


class TaskListView(LoginRequiredMixin, SearchMixin, ListView):
    model = Task
    paginate_by = 5
    search_fields = (
        "name",
        "description",
        "task_type__name",
        "assignees__username",
        "assignees__first_name",
        "assignees__last_name",
    )
    queryset = Task.objects.select_related("task_type").prefetch_related(
        "assignees"
    )

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.GET.get("filter") == "my":
            queryset = queryset.filter(assignees=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_filter"] = self.request.GET.get("filter", "")
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    queryset = Task.objects.select_related("task_type").prefetch_related(
        "assignees"
    )


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = (
        "name",
        "description",
        "deadline",
        "is_completed",
        "priority",
        "task_type",
        "assignees",
    )
    success_url = reverse_lazy("tasks:task-list")


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = (
        "name",
        "description",
        "deadline",
        "is_completed",
        "priority",
        "task_type",
        "assignees",
    )
    success_url = reverse_lazy("tasks:task-list")


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")


class WorkerListView(LoginRequiredMixin, SearchMixin, ListView):
    model = Worker
    paginate_by = 10
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "position__name",
    )
    queryset = Worker.objects.select_related("position")


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    queryset = Worker.objects.select_related("position")


class PositionListView(LoginRequiredMixin, SearchMixin, ListView):
    model = Position
    paginate_by = 10
    search_fields = ("name",)


class PositionCreateView(LoginRequiredMixin, CreateView):
    model = Position
    fields = ("name",)
    success_url = reverse_lazy("tasks:position-list")


class TaskTypeListView(LoginRequiredMixin, SearchMixin, ListView):
    model = TaskType
    paginate_by = 10
    search_fields = ("name",)
    template_name = "tasks/task_type_list.html"


class TaskTypeCreateView(LoginRequiredMixin, CreateView):
    model = TaskType
    fields = ("name",)
    success_url = reverse_lazy("tasks:task-type-list")
    template_name = "tasks/task_type_form.html"
