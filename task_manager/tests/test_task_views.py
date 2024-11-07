from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.forms import TaskForm
from task_manager.models import Task

TASK_LIST_URL = reverse("task-manager:task-list")
TASK_CREATE_URL = reverse("task-manager:task-create")
TASK_UPDATE_URL = reverse("task-manager:task-update", kwargs={"pk": 1})
TASK_DELETE_URL = reverse("task-manager:task-delete", kwargs={"pk": 1})


class TaskListTests(TestCase):
    fixtures = ["it_company_task_manager_db_data.json"]

    def setUp(self) -> None:
        self.user = get_user_model().objects.get(pk=1)
        self.client.force_login(self.user)

    def test_correct_template_used(self) -> None:
        response = self.client.get(TASK_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/task_list.html")

    def test_correct_filter(self) -> None:
        url_completed = TASK_LIST_URL + "?" + urlencode({"completed": "true"})
        url_pending = TASK_LIST_URL + "?" + urlencode({"completed": "false"})
        response_completed = self.client.get(url_completed)
        response_pending = self.client.get(url_pending)
        self.assertEqual(
            list(response_completed.context["task_list"]),
            list(Task.objects.filter(is_completed=True)),
        )
        self.assertEqual(
            list(response_pending.context["task_list"]),
            list(Task.objects.filter(is_completed=False)),
        )


class TaskCreateTests(TestCase):
    fixtures = ["it_company_task_manager_db_data.json"]

    def setUp(self) -> None:
        self.user = get_user_model().objects.get(pk=1)
        self.client.force_login(self.user)

    def test_correct_template_used(self) -> None:
        response = self.client.get(TASK_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/task_form.html")

    def test_correct_form_used(self) -> None:
        response = self.client.get(TASK_CREATE_URL)
        self.assertTrue(
            isinstance(response.context["form"],
                       TaskForm)
        )

    def test_correct_redirect_after_task_create(self) -> None:
        response = self.client.post(
            TASK_CREATE_URL,
            {
                "name": "test_task",
                "deadline": "2024-09-10T12:00:00Z",
                "priority": "HIGH",
                "assignees": [1]

            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, TASK_LIST_URL)

    def test_form_does_not_include_is_completed_field(self) -> None:
        response = self.client.get(TASK_CREATE_URL)
        self.assertNotIn("is_completed", response.context["form"].fields)


class TaskUpdateTests(TestCase):
    fixtures = ["it_company_task_manager_db_data.json"]

    def setUp(self) -> None:
        self.user = get_user_model().objects.get(pk=1)
        self.client.force_login(self.user)

    def test_correct_template_used(self) -> None:
        response = self.client.get(TASK_UPDATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/task_form.html")

    def test_correct_form_used(self) -> None:
        response = self.client.get(TASK_UPDATE_URL)
        self.assertTrue(
            isinstance(response.context["form"],
                       TaskForm)
        )

    def test_correct_redirect_after_task_update(self) -> None:
        response = self.client.post(
            TASK_UPDATE_URL,
            {
                "name": "test_task",
                "deadline": "2024-09-10T12:00:00Z",
                "priority": "HIGH",
                "assignees": [1]

            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, TASK_LIST_URL)

    def test_form_includes_is_completed_field(self) -> None:
        response = self.client.get(TASK_UPDATE_URL)
        self.assertIn("is_completed", response.context["form"].fields)


class TaskDeleteTests(TestCase):
    fixtures = ["it_company_task_manager_db_data.json"]

    def setUp(self) -> None:
        self.user = get_user_model().objects.get(pk=1)
        self.client.force_login(self.user)

    def test_correct_template_used(self) -> None:
        response = self.client.get(TASK_DELETE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "task_manager/task_confirm_delete.html"
        )

    def test_task_deleted(self) -> None:
        response = self.client.post(TASK_DELETE_URL)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=1).exists())

    def test_correct_redirect_after_task_delete(self) -> None:
        response = self.client.post(TASK_DELETE_URL)
        self.assertRedirects(response, TASK_LIST_URL)


class LoginRequiredTests(TestCase):
    def test_task_list_restricted_to_logged_in(self) -> None:
        response = self.client.get(TASK_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_task_create_restricted_to_logged_in(self) -> None:
        response = self.client.get(TASK_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_task_update_restricted_to_logged_in(self) -> None:
        response = self.client.get(TASK_UPDATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_task_delete_restricted_to_logged_in(self) -> None:
        response = self.client.get(TASK_DELETE_URL)
        self.assertNotEqual(response.status_code, 200)
