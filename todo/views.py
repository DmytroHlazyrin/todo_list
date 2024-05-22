from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView

from todo.models import Person, Tag, Task
from todo.forms import PersonCreationForm, PersonForm, SearchForm


def index(request):
    """View function for the home page of the site."""

    num_actions = Task.objects.count()
    num_person = Person.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_actions": num_actions,
        "num_person": num_person,
        "num_visits": num_visits + 1,
    }

    return render(request, "todo/index.html", context=context)


class SignUpView(generic.CreateView):
    form_class = PersonCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 10
    template_name = "todo/index.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = SearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Task.objects.prefetch_related("tags")
        form = SearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "todo/task_detail.html"


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("todo:task-detail")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("todo:task-detail")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("todo:action-list")
    template_name = "todo/task_confirm_delete.html"


class PersonListView(LoginRequiredMixin, generic.ListView):
    model = Person
    success_url = reverse_lazy("todo:person-list")
    context_object_name = "persons"
    paginate_by = 4


class PersonUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Person
    form_class = PersonForm
    template_name = "todo/person_update.html"
    success_url = reverse_lazy("todo:person-detail")


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    template_name = "todo/tag_list.html"
    context_object_name = "tag_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = SearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Tag.objects.all()
        form = SearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    fields = "__all__"


class TagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    fields = "__all__"


class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("todo:tag-list")
    template_name = "todo/tag_confirm_delete.html"


@login_required
def change_status(request, pk):
    task = Task.objects.get(pk=pk)
    task.change_status()
    task.save()
    messages.success(
        request, f"Status for {task.name} has been changed!"
    )
    return HttpResponseRedirect(reverse_lazy("todo:index"))


