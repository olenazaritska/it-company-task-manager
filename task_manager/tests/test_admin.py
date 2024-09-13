from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import formats

from task_manager.models import Task


class AdminSiteTests(TestCase):
    fixtures = ["it_company_task_manager_db_data.json"]

    def convert_deadline(self, deadline: datetime) -> str:
        formatted_date = formats.date_format(deadline, "N j, Y")

        if deadline.hour == 12 and deadline.minute == 0:
            formatted_time = "noon"
        elif deadline.hour == 0 and deadline.minute == 0:
            formatted_time = "midnight"
        else:
            formatted_time = formats.time_format(deadline, "g:i a")

        formatted_datetime = f"{formatted_date}, {formatted_time}"

        return formatted_datetime

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.get(pk=1)
        self.client.force_login(self.admin_user)

    def test_worker_list_display_has_position(self) -> None:
        url = reverse("admin:task_manager_worker_changelist")
        response = self.client.get(url)
        self.assertContains(
            response,
            get_user_model().objects.get(pk=1).position
        )

    def test_worker_change_has_position(self) -> None:
        url = reverse("admin:task_manager_worker_change", args=[1])
        response = self.client.get(url)
        self.assertContains(
            response,
            get_user_model().objects.get(pk=1).position
        )

    def test_worker_add_had_additional_info(self) -> None:
        url = reverse("admin:task_manager_worker_add")
        response = self.client.get(url)
        self.assertContains(response, "Additional info")
        self.assertContains(response, "Email address:")
        self.assertContains(response, "First name:")
        self.assertContains(response, "Last name:")
        self.assertContains(response, "Position:")
        self.assertContains(response, "Staff status")

    def test_task_list_display_has_all_required_fields(self) -> None:
        url = reverse("admin:task_manager_task_changelist")
        response = self.client.get(url)
        self.assertContains(response, Task.objects.get(pk=1).name)
        self.assertContains(
            response,
            self.convert_deadline(Task.objects.get(pk=1).deadline)
        )
        self.assertContains(response, Task.objects.get(pk=1).is_completed)
        self.assertContains(response, Task.objects.get(pk=1).priority)
        self.assertContains(response, Task.objects.get(pk=1).task_type)
        self.assertContains(
            response,
            ", ".join(
                [
                    f"{a.first_name} {a.last_name}"
                    for a in Task.objects.get(pk=1).assignees.all()
                ]
            )
        )

    def test_task_list_display_has_search_field(self) -> None:
        url = reverse("admin:task_manager_task_changelist")
        response = self.client.get(url)
        self.assertContains(
            response,
            '<input type="submit" value="Search">'
        )

    def test_task_list_display_has_all_filters(self) -> None:
        url = reverse("admin:task_manager_task_changelist")
        response = self.client.get(url)
        self.assertContains(response, "By priority")
        self.assertContains(response, "By deadline")
        self.assertContains(response, "By is completed")
        self.assertContains(response, "By task type")
        self.assertContains(response, "By assignees")
