from datetime import timedelta

from django.db.models import Count, Q
from django.utils import timezone

from .models import Category, Todo


def sidebar(request):
    """Adds sidebar counts and categories to every template automatically."""
    if not request.user.is_authenticated:
        return {}

    today = timezone.localdate()
    todos = Todo.objects.filter(user=request.user)

    counts = todos.aggregate(
        all=Count("srno"),
        active=Count("srno", filter=Q(completed=False)),
        today=Count("srno", filter=Q(completed=False, due_date=today)),
        upcoming=Count(
            "srno",
            filter=Q(completed=False, due_date__gt=today, due_date__lte=today + timedelta(days=7)),
        ),
        overdue=Count("srno", filter=Q(completed=False, due_date__lt=today)),
        completed=Count("srno", filter=Q(completed=True)),
    )

    categories = Category.objects.filter(user=request.user).annotate(
        open_count=Count("todos", filter=Q(todos__completed=False))
    )

    return {"nav_counts": counts, "nav_categories": categories}