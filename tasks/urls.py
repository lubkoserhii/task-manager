from django.urls import path

from .views import (
    HomeView,
    PositionCreateView,
    PositionListView,
    TaskCreateView,
    TaskDeleteView,
    TaskDetailView,
    TaskListView,
    TaskTypeCreateView,
    TaskTypeListView,
    TaskUpdateView,
    WorkerDetailView,
    WorkerListView,
    WorkerRegisterView,
    TaskToggleStatusView,
)

app_name = "tasks"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path(
        "tasks/<int:pk>/toggle-status/",
        TaskToggleStatusView.as_view(),
        name="task-toggle-status",
    ),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("task-types/", TaskTypeListView.as_view(), name="task-type-list"),
    path(
        "task-types/create/",
        TaskTypeCreateView.as_view(),
        name="task-type-create",
    ),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("register/", WorkerRegisterView.as_view(), name="register"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/create/", PositionCreateView.as_view(), name="position-create"),
]
