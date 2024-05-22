from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Person, Task, Tag


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("id",) + UserAdmin.list_display


@admin.register(Task)
class ActionAdmin(admin.ModelAdmin):
    list_display = [
        "id", "name", "author",
    ]
    search_fields = [
        "name",
        "author",
    ]


admin.site.register(Tag)
