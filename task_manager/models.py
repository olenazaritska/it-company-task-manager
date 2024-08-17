from django.contrib.auth.models import AbstractUser
from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        choices=[
            ("HIGH", "High"),
            ("MEDIUM", "Medium"),
            ("LOW", "Low"),
        ],
        max_length=255
    )
    task_type = models.ForeignKey(
        "TaskType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks"
    )
    assignees = models.ManyToManyField("Worker", related_name="tasks")


class TaskType(models.Model):
    name = models.CharField(max_length=255)


class Worker(AbstractUser):
    position = models.ForeignKey(
        "Position",
        on_delete=models.CASCADE,
        related_name="workers"
    )


class Position(models.Model):
    name = models.CharField(max_length=255)
