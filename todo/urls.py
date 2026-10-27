from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import RedirectView

from . import views
from .forms import LoginForm

app_name = "todo"

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="todo:dashboard"), name="home"),

    path("sign-up/", views.signup_view, name="sign_up"),
    path(
        "log-in/",
        auth_views.LoginView.as_view(
            template_name="authentication/login.html",
            authentication_form=LoginForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("log-out/", auth_views.LogoutView.as_view(), name="logout"),

    path("dashboard/", views.dashboard, name="dashboard"),
    path("tasks/", views.task_list, name="tasks"),
    path("tasks/new/", views.task_create, name="task_create"),
    path("tasks/<int:srno>/edit/", views.task_edit, name="task_edit"),
    path("tasks/<int:srno>/delete/", views.task_delete, name="task_delete"),
    path("tasks/<int:srno>/toggle/", views.task_toggle, name="task_toggle"),
    path("tasks/clear-completed/", views.clear_completed, name="clear_completed"),
    path("categories/", views.categories, name="categories"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),
    path("profile/", views.profile, name="profile"),
]