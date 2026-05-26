from django.test import TestCase

from tasks.forms import WorkerCreationForm
from tasks.models import Position, Worker


class WorkerCreationFormTests(TestCase):
    def test_form_has_position_field(self):
        form = WorkerCreationForm()

        self.assertIn("position", form.fields)

    def test_form_creates_worker_with_position(self):
        position = Position.objects.create(name="Developer")
        form = WorkerCreationForm(
            data={
                "username": "new.worker",
                "password1": "StrongPass123",
                "password2": "StrongPass123",
                "position": position.pk,
            }
        )

        self.assertTrue(form.is_valid())
        worker = form.save()

        self.assertEqual(worker.position, position)
        self.assertTrue(Worker.objects.filter(username="new.worker").exists())
