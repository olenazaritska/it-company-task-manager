from django import forms
from django.test import TestCase
from formset.widgets import DateTimeInput

from task_manager.forms import WorkerCreationForm, WorkerUpdateForm, TaskForm
from task_manager.models import Position


class WorkerCreationFormTest(TestCase):
    fixtures = ["it_company_task_manager_db_data.json"]

    def test_form_has_all_fields_specified(self) -> None:
        form = WorkerCreationForm()
        expected_fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "position",
            "password1",
            "password2",
            "usable_password"
        ]
        self.assertEqual(
            list(form.fields.keys()),
            expected_fields
        )

    def test_worker_creation_form_is_valid(self) -> None:
        data = {
            "username": "test_user",
            "email": "email@example.com",
            "first_name": "first_name",
            "last_name": "last_name",
            "position": Position.objects.first(),
            "password1": "1qazcde3",
            "password2": "1qazcde3",
        }
        form = WorkerCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_worker_creation_form_is_not_valid(self) -> None:
        data = {
            "username": "test_user",
            "email": "email",
            "first_name": "first_name",
            "last_name": "last_name",
            "position": Position.objects.first(),
            "password1": "",
            "password2": "1qazcde3",
        }
        form = WorkerCreationForm(data=data)
        self.assertFalse(form.is_valid())


class WorkerUpdateFormTest(TestCase):
    fixtures = ["it_company_task_manager_db_data.json"]

    def test_form_has_all_fields_specified(self) -> None:
        form = WorkerUpdateForm()
        expected_fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "position",
            "password1",
            "password2",
        ]
        self.assertEqual(
            list(form.fields.keys()),
            expected_fields
        )

    def test_worker_update_form_is_valid_with_no_password(self) -> None:
        data = {
            "username": "test_user",
            "email": "email@example.com",
            "first_name": "first_name",
            "last_name": "last_name",
            "position": Position.objects.first(),
        }
        form = WorkerUpdateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_worker_update_form_is_not_valid_with_no_password(self) -> None:
        data = {
            "username": "test_user",
            "email": "email@example.com",
            "first_name": "first_name",
            "last_name": "last_name",
        }
        form = WorkerUpdateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_worker_update_form_is_valid_with_password(self) -> None:
        data = {
            "username": "test_user",
            "email": "email@example.com",
            "first_name": "first_name",
            "last_name": "last_name",
            "position": Position.objects.first(),
            "password1": "1qazcde3",
            "password2": "1qazcde3",
        }
        form = WorkerUpdateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_worker_update_form_is_not_valid_with_password(self) -> None:
        data = {
            "username": "test_user",
            "email": "email@example.com",
            "first_name": "first_name",
            "last_name": "last_name",
            "position": Position.objects.first(),
            "password1": "123",
            "password2": "123",
        }
        form = WorkerUpdateForm(data=data)
        self.assertFalse(form.is_valid())


class TaskFormTest(TestCase):
    fixtures = ["it_company_task_manager_db_data.json"]

    def test_form_has_all_fields_specified(self) -> None:
        form = TaskForm()
        expected_fields = [
            "name",
            "description",
            "deadline",
            "is_completed",
            "priority",
            "task_type",
            "assignees"
        ]
        self.assertEqual(
            list(form.fields.keys()),
            expected_fields
        )

    def test_deadline_field_is_datetimeinput(self) -> None:
        form = TaskForm()
        self.assertIsInstance(form.fields["deadline"].widget, DateTimeInput)

    def test_assignees_field_is_checkboxselectmultiple(self) -> None:
        form = TaskForm()
        self.assertIsInstance(
            form.fields["assignees"].widget,
            forms.CheckboxSelectMultiple
        )

    def test_task_form_is_valid(self) -> None:
        data = {
            "name": "test_task",
            "deadline": "2024-09-20T12:00:00Z",
            "priority": "MEDIUM",
            "assignees": [1, 2]
        }
        form = TaskForm(data=data)
        self.assertTrue(form.is_valid())

    def test_task_form_is_not_valid(self) -> None:
        data = {
            "name": "test_task",
            "deadline": "2024-09-20T12:00:00Z",
            "priority": "MEDIUM",
        }
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())
