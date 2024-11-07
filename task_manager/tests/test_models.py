from django.contrib.auth import get_user_model
from django.test import TestCase

from task_manager.models import Task, TaskType, Position


class ModelsTest(TestCase):
    fixtures = ["it_company_task_manager_db_data.json"]

    def test_task_str(self) -> None:
        task = Task.objects.create(
            name="test_task",
            deadline="2024-09-20T12:00:00Z",
            priority="LOW"
        )
        task.assignees.set(
            (
                get_user_model().objects.get(pk=1),
            )
        )
        self.assertEqual(str(task), task.name)

    def test_task_type_str(self) -> None:
        task_type = TaskType.objects.create(
            name="test_task_type",
        )
        self.assertEqual(str(task_type), task_type.name)

    def test_worker_str(self) -> None:
        worker = get_user_model().objects.create(
            username="test_worker",
            password="test_password",
            first_name="test_first_name",
            last_name="test_last_name",
            position=Position.objects.get(pk=1),
        )
        self.assertEqual(
            str(worker),
            f"{worker.first_name} {worker.last_name} ({worker.position.name})"
        )

    def test_create_worker_with_position(self) -> None:
        worker = get_user_model().objects.create(
            username="test_worker",
            password="test_password",
            first_name="test_first_name",
            last_name="test_last_name",
            position=Position.objects.get(pk=1),
        )
        self.assertEqual(worker.position, Position.objects.get(pk=1))

    def test_position_str(self) -> None:
        position = Position.objects.create(
            name="test_position",
        )
        self.assertEqual(str(position), position.name)
