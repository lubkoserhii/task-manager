from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from tasks.models import Task, TaskType


class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test.user",
            password="testpass123",
        )
        cls.task_type = TaskType.objects.create(name="Bug")

    def test_task_list_requires_login(self):
        response = self.client.get(reverse("tasks:task-list"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response["Location"])

    def test_home_view_shows_statistics(self):
        Task.objects.create(
            name="Open task",
            deadline=date.today(),
            task_type=self.task_type,
        )
        Task.objects.create(
            name="Completed task",
            deadline=date.today(),
            is_completed=True,
            task_type=self.task_type,
        )
        self.client.force_login(self.user)

        response = self.client.get(reverse("tasks:home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_tasks"], 2)
        self.assertEqual(response.context["num_completed_tasks"], 1)
        self.assertEqual(response.context["num_workers"], 1)

    def test_task_list_is_paginated(self):
        today = timezone.localdate()
        tasks = [
            Task(
                name=f"Task {index}",
                deadline=today + timedelta(days=index),
                task_type=self.task_type,
            )
            for index in range(6)
        ]
        Task.objects.bulk_create(tasks)
        self.client.force_login(self.user)

        response = self.client.get(reverse("tasks:task-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["task_list"]), 5)

    def test_task_list_search_filters_results(self):
        Task.objects.create(
            name="Fix dashboard",
            deadline=date.today(),
            task_type=self.task_type,
        )
        Task.objects.create(
            name="Add profile page",
            deadline=date.today(),
            task_type=self.task_type,
        )
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("tasks:task-list"),
            {"q": "dashboard"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["task_list"],
            ["Fix dashboard"],
            transform=str,
        )
