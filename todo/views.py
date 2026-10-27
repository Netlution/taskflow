from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Case, Count, IntegerField, Q, Value, When
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import CategoryForm, ProfileForm, SignUpForm, TodoForm
from .models import Category, Todo


def go_back(request, fallback="todo:dashboard"):
    next_url = request.POST.get("next") or request.GET.get("next")
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect(fallback)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("todo:dashboard")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            for name, color in [("Work", "indigo"), ("Personal", "emerald"), ("Shopping", "amber")]:
                Category.objects.create(user=user, name=name, color=color)
            messages.success(request, f"Welcome aboard, {user.first_name}! Your workspace is ready.")
            return redirect("todo:dashboard")
    else:
        form = SignUpForm()
    return render(request, "authentication/signup.html", {"form": form})


@login_required
def dashboard(request):
    today = timezone.localdate()
    todos = Todo.objects.filter(user=request.user).select_related("category")

    total = todos.count()
    completed = todos.filter(completed=True).count()
    pending = total - completed
    overdue_qs = todos.filter(completed=False, due_date__lt=today)

    week = []
    for days_ago in range(6, -1, -1):
        day = today - timedelta(days=days_ago)
        week.append({"label": day.strftime("%a"), "count": todos.filter(completed_at__date=day).count()})
    week_max = max([d["count"] for d in week] + [1])
    for d in week:
        d["height"] = round(d["count"] / week_max * 100)

    categories = (
        Category.objects.filter(user=request.user)
        .annotate(total=Count("todos"), done=Count("todos", filter=Q(todos__completed=True)))
        .filter(total__gt=0)
    )
    for c in categories:
        c.percent = round(c.done / c.total * 100)

    context = {
        "form": TodoForm(user=request.user),
        "stats": {
            "total": total,
            "completed": completed,
            "pending": pending,
            "overdue": overdue_qs.count(),
            "rate": round(completed / total * 100) if total else 0,
        },
        "due_today": todos.filter(completed=False, due_date=today),
        "overdue": overdue_qs[:5],
        "upcoming": todos.filter(
            completed=False, due_date__gt=today, due_date__lte=today + timedelta(days=7)
        )[:5],
        "recent_done": todos.filter(completed=True).order_by("-completed_at")[:5],
        "high_priority": todos.filter(completed=False, priority="high").count(),
        "week": week,
        "week_total": sum(d["count"] for d in week),
        "categories": categories,
        "today": today,
    }
    return render(request, "dashboard.html", context)


@login_required
def task_list(request):
    today = timezone.localdate()
    todos = Todo.objects.filter(user=request.user).select_related("category")

    status = request.GET.get("status", "all")
    priority = request.GET.get("priority", "")
    category = request.GET.get("category", "")
    query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "due")

    if status == "active":
        todos = todos.filter(completed=False)
    elif status == "completed":
        todos = todos.filter(completed=True)
    elif status == "today":
        todos = todos.filter(completed=False, due_date=today)
    elif status == "upcoming":
        todos = todos.filter(completed=False, due_date__gt=today, due_date__lte=today + timedelta(days=7))
    elif status == "overdue":
        todos = todos.filter(completed=False, due_date__lt=today)

    if priority:
        todos = todos.filter(priority=priority)
    if category:
        todos = todos.filter(category__pk=category)
    if query:
        todos = todos.filter(Q(title__icontains=query) | Q(description__icontains=query))

    if sort == "newest":
        todos = todos.order_by("completed", "-created_at")
    elif sort == "priority":
        rank = Case(
            When(priority="high", then=Value(0)),
            When(priority="medium", then=Value(1)),
            default=Value(2),
            output_field=IntegerField(),
        )
        todos = todos.annotate(rank=rank).order_by("completed", "rank", "-created_at")

    titles = {
        "all": "All tasks", "active": "Active", "completed": "Completed",
        "today": "Due today", "upcoming": "Next 7 days", "overdue": "Overdue",
    }
    selected_category = Category.objects.filter(user=request.user, pk=category).first() if category else None

    context = {
        "todos": todos,
        "status": status,
        "priority": priority,
        "category": category,
        "q": query,
        "sort": sort,
        "page_title": selected_category.name if selected_category else titles.get(status, "All tasks"),
        "categories": Category.objects.filter(user=request.user),
        "priorities": Todo.PRIORITY_CHOICES,
    }
    return render(request, "tasks/task_list.html", context)


@login_required
def task_create(request):
    if request.method == "POST":
        form = TodoForm(request.POST, user=request.user)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, f"“{todo.title}” added.")
            return go_back(request, fallback="todo:tasks")
    else:
        form = TodoForm(user=request.user, initial={"category": request.GET.get("category")})
    return render(request, "tasks/task_form.html", {"form": form, "is_edit": False})


@login_required
def task_edit(request, srno):
    todo = get_object_or_404(Todo, srno=srno, user=request.user)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated.")
            return go_back(request, fallback="todo:tasks")
    else:
        form = TodoForm(instance=todo, user=request.user)
    return render(request, "tasks/task_form.html", {"form": form, "todo": todo, "is_edit": True})


@login_required
def task_delete(request, srno):
    todo = get_object_or_404(Todo, srno=srno, user=request.user)
    if request.method == "POST":
        title = todo.title
        todo.delete()
        messages.success(request, f"“{title}” deleted.")
        return go_back(request, fallback="todo:tasks")
    return render(request, "tasks/task_confirm_delete.html", {"todo": todo})


@login_required
@require_POST
def task_toggle(request, srno):
    todo = get_object_or_404(Todo, srno=srno, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    if todo.completed:
        messages.success(request, f"Nice work! “{todo.title}” is done.")
    return go_back(request)


@login_required
@require_POST
def clear_completed(request):
    count, _ = Todo.objects.filter(user=request.user, completed=True).delete()
    messages.success(request, f"Cleared {count} completed task{'s' if count != 1 else ''}.")
    return redirect("todo:tasks")


@login_required
def categories(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, user=request.user)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.user = request.user
            cat.save()
            messages.success(request, f"Category “{cat.name}” created.")
            return redirect("todo:categories")
    else:
        form = CategoryForm(user=request.user)

    cats = Category.objects.filter(user=request.user).annotate(
        total=Count("todos"), open_count=Count("todos", filter=Q(todos__completed=False))
    )
    return render(request, "categories.html", {"form": form, "cats": cats})


@login_required
@require_POST
def category_delete(request, pk):
    cat = get_object_or_404(Category, pk=pk, user=request.user)
    name = cat.name
    cat.delete()
    messages.success(request, f"Category “{name}” deleted. Its tasks were kept.")
    return redirect("todo:categories")


@login_required
def profile(request):
    profile_form = ProfileForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)

    if request.method == "POST":
        if request.POST.get("action") == "profile":
            profile_form = ProfileForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile updated.")
                return redirect("todo:profile")
        elif request.POST.get("action") == "password":
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed.")
                return redirect("todo:profile")

    todos = Todo.objects.filter(user=request.user)
    context = {
        "profile_form": profile_form,
        "password_form": password_form,
        "total": todos.count(),
        "done": todos.filter(completed=True).count(),
    }
    return render(request, "profile.html", context)