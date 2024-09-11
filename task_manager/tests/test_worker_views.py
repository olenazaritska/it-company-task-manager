from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.forms import WorkerCreationForm, WorkerUpdateForm
from task_manager.models import Task

WORKER_LIST_URL = reverse("task-manager:worker-list")
WORKER_DETAIL_URL = reverse("task-manager:worker-detail", kwargs={"pk": 1})
WORKER_CREATE_URL = reverse("task-manager:worker-create")
WORKER_UPDATE_URL = reverse("task-manager:worker-update", kwargs={"pk": 1})
WORKER_DELETE_URL = reverse("task-manager:worker-delete", kwargs={"pk": 1})


class WorkerListTests(TestCase):
    fixtures = ["it_company_task_manager_db_data.json"]

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.client.force_login(self.user)

    def test_correct_template_used(self):
        response = self.client.get(WORKER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/worker_list.html")

    def test_correct_pagination(self):
        response = self.client.get(WORKER_LIST_URL)
        self.assertEqual(len(response.context["worker_list"]), 4)


class WorkerDetailTests(TestCase):
    fixtures = ["it_company_task_manager_db_data.json"]

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.client.force_login(self.user)

    def test_correct_template_used(self):
        response = self.client.get(WORKER_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/worker_detail.html")

    def test_correct_task_count(self):
        worker_tasks = get_user_model().objects.get(pk=1).tasks
        response = self.client.get(WORKER_DETAIL_URL)
        self.assertIn("completed_tasks_count", response.context)
        self.assertIn("pending_tasks_count", response.context)
        self.assertEqual(
            response.context["completed_tasks_count"],
            worker_tasks.filter(is_completed=True).count(),
        )
        self.assertEqual(
            response.context["pending_tasks_count"],
            worker_tasks.filter(is_completed=False).count(),
        )

    def test_correct_pending_tasks(self):
        worker_tasks = get_user_model().objects.get(pk=1).tasks
        response = self.client.get(WORKER_DETAIL_URL)
        self.assertIn("pending_tasks", response.context)
        self.assertEqual(
            list(response.context["pending_tasks"]),
            list(worker_tasks.filter(is_completed=False))
        )
        for task in response.context["pending_tasks"]:
            all_task_assignees = Task.objects.get(pk=task.pk).assignees
            self.assertEqual(
                list(task.other_assignees),
                list(
                    all_task_assignees.exclude(id=self.user.id)
                ),
            )


class WorkerCreateTests(TestCase):
    fixtures = ["it_company_task_manager_db_data.json"]

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.client.force_login(self.user)

    def test_correct_template_used(self):
        response = self.client.get(WORKER_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/worker_form.html")

    def test_correct_form_used(self):
        response = self.client.get(WORKER_CREATE_URL)
        self.assertTrue(
            isinstance(response.context["form"],
                       WorkerCreationForm)
        )

    def test_correct_redirect_after_worker_create(self):
        response = self.client.post(
            WORKER_CREATE_URL,
            {
                "username": "new_user",
                "password1": "test_password",
                "password2": "test_password",
                "position": 1,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, WORKER_LIST_URL)


class WorkerUpdateTests(TestCase):
    fixtures = ["it_company_task_manager_db_data.json"]

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.client.force_login(self.user)

    def test_correct_template_used(self):
        response = self.client.get(WORKER_UPDATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/worker_form.html")

    def test_correct_form_used(self):
        response = self.client.get(WORKER_UPDATE_URL)
        self.assertTrue(
            isinstance(response.context["form"],
                       WorkerUpdateForm)
        )

    def test_correct_redirect_after_worker_update(self):
        response = self.client.post(
            WORKER_UPDATE_URL,
            {
                "username": "test_username",
                "position": 2,
                "password": "test_password",
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, WORKER_DETAIL_URL)

    def test_update_available_to_logged_in_user_only(self):
        response = self.client.get(
            reverse("task-manager:worker-update", kwargs={"pk": 2})
        )
        self.assertEqual(response.status_code, 403)


class WorkerDeleteTests(TestCase):
    fixtures = ["it_company_task_manager_db_data.json"]

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.client.force_login(self.user)

    def test_correct_template_used(self):
        response = self.client.get(WORKER_DELETE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "task_manager/worker_confirm_delete.html"
        )

    def test_worker_deleted(self):
        response = self.client.post(WORKER_DELETE_URL)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(get_user_model().objects.filter(pk=1).exists())

    def test_correct_redirect_after_delete_other_worker(self):
        response = self.client.post(
            reverse("task-manager:worker-delete", kwargs={"pk": 2})
        )
        self.assertRedirects(response, WORKER_LIST_URL)

    def test_correct_redirect_after_delete_yourself(self):
        response = self.client.post(WORKER_DELETE_URL)
        self.assertRedirects(response, WORKER_LIST_URL, target_status_code=302)


class LoginRequiredTests(TestCase):
    def test_worker_list_restricted_to_logged_in(self):
        response = self.client.get(WORKER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_worker_detail_restricted_to_logged_in(self):
        response = self.client.get(WORKER_DETAIL_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_worker_create_restricted_to_logged_in(self):
        response = self.client.get(WORKER_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_worker_update_restricted_to_logged_in(self):
        response = self.client.get(WORKER_UPDATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_worker_delete_restricted_to_logged_in(self):
        response = self.client.get(WORKER_DELETE_URL)
        self.assertNotEqual(response.status_code, 200)
