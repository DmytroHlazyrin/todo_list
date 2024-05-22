from django.urls import path

from todo.views import index, PersonUpdateView, TagListView, TaskListView, TagCreateView, TagUpdateView, TagDeleteView, \
    change_status, TaskDetailView, TaskUpdateView, TaskDeleteView, TaskCreateView

app_name = "todo"

urlpatterns = [
    path("", TaskListView.as_view(), name="index"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("task/create/", TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("tags/", TagListView.as_view(), name="tag-list"),
    path("person/<int:pk>/update/", PersonUpdateView.as_view(), name="person-update"),
    path(
        "tags/create/",
        TagCreateView.as_view(),
        name="tag-create",
    ),
    path(
        "tags/<int:pk>/update/",
        TagUpdateView.as_view(),
        name="tag-update",
    ),
    path(
        "tags/<int:pk>/delete/",
        TagDeleteView.as_view(),
        name="tag-delete",
    ),
    path("tags/<int:pk>/change_status/", change_status, name="change-status"),

]


