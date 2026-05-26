from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Position, Task, TaskType, Worker


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Work info", {"fields": ("position",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Work info", {"fields": ("position",)}),
    )
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "position",
        "is_staff",
    )
    list_filter = UserAdmin.list_filter + ("position",)
    search_fields = ("username", "email", "first_name", "last_name")
    list_select_related = ("position",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "task_type",
        "priority",
        "deadline",
        "is_completed",
    )
    list_filter = ("is_completed", "priority", "task_type", "deadline")
    search_fields = ("name", "description", "assignees__username")
    filter_horizontal = ("assignees",)
    list_select_related = ("task_type",)
