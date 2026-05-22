from django.contrib import admin
from django.test import SimpleTestCase

from tasks.admin import TaskAdmin, WorkerAdmin
from tasks.models import Position, Task, TaskType, Worker


class AdminTests(SimpleTestCase):
    def test_models_are_registered_in_admin(self):
        self.assertIn(Position, admin.site._registry)
        self.assertIn(TaskType, admin.site._registry)
        self.assertIn(Worker, admin.site._registry)
        self.assertIn(Task, admin.site._registry)

    def test_worker_admin_has_position_configuration(self):
        worker_admin = admin.site._registry[Worker]

        self.assertIsInstance(worker_admin, WorkerAdmin)
        self.assertIn("position", worker_admin.list_display)
        self.assertIn("position", worker_admin.list_select_related)

    def test_task_admin_has_custom_configuration(self):
        task_admin = admin.site._registry[Task]

        self.assertIsInstance(task_admin, TaskAdmin)
        self.assertIn("assignees", task_admin.filter_horizontal)
        self.assertIn("task_type", task_admin.list_select_related)
