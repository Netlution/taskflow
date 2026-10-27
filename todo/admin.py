from django.contrib import admin

from .models import Category, Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("srno", "title", "user", "category", "priority", "due_date", "completed")
    list_filter = ("completed", "priority", "category")
    search_fields = ("title", "description")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "color")
# Register your models here.
