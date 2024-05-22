from django import forms
from django.contrib.auth.forms import UserCreationForm

from todo.models import Person, Task, Tag


class PersonCreationForm(UserCreationForm):
    class Meta:
        model = Person
        fields = ("username", "email", "first_name", "last_name")


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ("username", "email", "first_name", "last_name")


class SearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class TaskForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "deadline": forms.DateTimeInput(attrs={"type": "datetime"})
        }

