from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Category, Todo


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label="First name")
    email = forms.EmailField(label="Email address")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "first_name": "Newton",
            "username": "Choose a username",
            "email": "you@example.com",
            "password1": "Create a password",
            "password2": "Repeat your password",
        }
        for name, text in placeholders.items():
            self.fields[name].widget.attrs["placeholder"] = text
            self.fields[name].help_text = ""  # keep the page clean; errors still show

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "Your username"
        self.fields["password"].widget.attrs["placeholder"] = "Your password"


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "description", "category", "priority", "due_date"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "What needs to be done?"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Add details (optional)"}),
            "due_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show the logged-in user's own categories in the dropdown.
        self.fields["category"].queryset = Category.objects.filter(user=user)
        self.fields["category"].empty_label = "No category"


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "color"]
        widgets = {"name": forms.TextInput(attrs={"placeholder": "e.g. Work"})}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if Category.objects.filter(user=self.user, name__iexact=name).exists():
            raise forms.ValidationError("You already have a category with this name.")
        return name


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]