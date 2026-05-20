from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workers",
    )

    class Meta:
        ordering = ("username",)

    def __str__(self) -> str:
        full_name = self.get_full_name()
        return full_name or self.username


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("urgent", "Urgent"),
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="medium",
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.PROTECT,
        related_name="tasks",
    )
    assignees = models.ManyToManyField(
        Worker,
        related_name="tasks",
        blank=True,
    )

    class Meta:
        ordering = ("deadline", "name")

    def __str__(self) -> str:
        return self.name
