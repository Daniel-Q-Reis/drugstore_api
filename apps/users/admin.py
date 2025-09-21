from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):  # type: ignore[type-arg]
    """
    Custom admin configuration for the User model.
    """

    list_display = ("email", "username", "first_name", "last_name", "is_staff")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("email",)
