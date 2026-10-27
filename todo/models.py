from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from django.utils import timezone


class Category(models.Model):
    """A label the user groups tasks under, e.g. Work, Personal, Shopping."""

    COLOR_CHOICES = [
        ("indigo", "Indigo"),
        ("emerald", "Emerald"),
        ("amber", "Amber"),
        ("rose", "Rose"),
        ("sky", "Sky"),
        ("violet", "Violet"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=40)
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, default="indigo")

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"
        constraints = [
            models.UniqueConstraint(fields=["user", "name"], name="unique_category_per_user")
        ]

    def __str__(self):
        return self.name


class Todo(models.Model):
    """A single task."""

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    srno = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todos")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="todos"
    )
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Unfinished first, then soonest due date (no date last), then newest.
        ordering = ["completed", F("due_date").asc(nulls_last=True), "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Record when the task was finished; clear it if the task is reopened.
        if self.completed and self.completed_at is None:
            self.completed_at = timezone.now()
        elif not self.completed:
            self.completed_at = None
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        return (
            not self.completed
            and self.due_date is not None
            and self.due_date < timezone.localdate()
        )

    @property
    def is_due_today(self):
        return not self.completed and self.due_date == timezone.localdate()