from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import fields
from formset.widgets import DateTimeInput

from task_manager.models import Worker, Task


class WorkerForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position",
        )


class TaskForm(forms.ModelForm):
    deadline = fields.DateTimeField(
        widget=DateTimeInput,
    )
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Task
        fields = "__all__"
