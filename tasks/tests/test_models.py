from datetime import date

from django.test import TestCase

from tasks.models import Position, Task, TaskType, Worker


class ModelTests(TestCase):
    def test_models_str_methods(self):
        position = Position.objects.create(name="Developer")
        task_type = TaskType.objects.create(name="Bug")
        worker = Worker.objects.create_user(
            username="john.dev",
            first_name="John",
            last_name="Doe",
            position=position,
        )
        task = Task.objects.create(
            name="Fix dashboard",
            description="Fix dashboard page",
            deadline=date(2026, 5, 22),
            task_type=task_type,
        )

        self.assertEqual(str(position), "Developer")
        self.assertEqual(str(task_type), "Bug")
        self.assertEqual(str(worker), "John Doe")
        self.assertEqual(str(task), "Fix dashboard")

    def test_worker_str_falls_back_to_username(self):
        worker = Worker.objects.create_user(username="qa.user")

        self.assertEqual(str(worker), "qa.user")
