from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from task_manager.models import Task, TaskType, Worker, Position


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "email",
                        "first_name",
                        "last_name",
                        "position",
                        "is_staff",
                    )
                },
            ),
        )
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "deadline",
        "is_completed",
        "priority",
        "task_type",
        "get_assignees",
    )

    search_fields = ("name",)
    list_filter = (
        "priority",
        "deadline",
        "is_completed",
        "task_type",
        "assignees",
    )

    def get_assignees(self, obj):
        return ", ".join(
            [f"{a.first_name} {a.last_name}" for a in obj.assignees.all()]
        )


admin.site.register(TaskType)
admin.site.register(Position)
