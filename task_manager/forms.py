from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.forms import fields
from formset.widgets import DateTimeInput

from task_manager.models import Worker, Task


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "email",
            "first_name",
            "last_name",
            "position",
        )


class WorkerUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        required=False,
        help_text="Leave blank if not changing"
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
        required=False,
        help_text="Leave blank if not changing"
    )

    class Meta:
        model = Worker
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "position",
        )

    def clean_password1(self) -> str | None:
        password1 = self.cleaned_data.get("password1")
        if password1:
            validate_password(password1, self.instance)
        return password1

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    "password1",
                    "The two password fields must match."
                )
        return cleaned_data

    def save(self, commit: bool = True) -> Worker:
        worker = super().save(commit=False)
        password1 = self.cleaned_data.get("password1")

        if password1:
            worker.password = make_password(password1)

        if commit:
            worker.save()
        return worker


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
