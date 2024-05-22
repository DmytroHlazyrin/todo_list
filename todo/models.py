from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Position"
        verbose_name_plural = "Positions"

    def __str__(self):
        return self.name


class Action(models.Model):
    STATUS_CHOICES = (
        ("not started", "Not started"),
        ("done", "Done"),
        ("do", "In progress"),
        ("problems", "Problems"),
        ("postponed", "Postponed"),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    priority = models.IntegerField(validators=[MinValueValidator(1),
                                               MaxValueValidator(5)])
    performers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name="actions")
    tags = models.ManyToManyField(Tag, related_name="actions")

    class Meta:
        verbose_name = "Action"
        verbose_name_plural = "Actions"

    def __str__(self):
        return self.name


class Comment(models.Model):
    action = models.ForeignKey(Action,
                               on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"Comment by {self.author} on {self.action}"


class Person(AbstractUser):
    position = models.ForeignKey(Position,
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Persons"

    def __str__(self):
        return self.username
