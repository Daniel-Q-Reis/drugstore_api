from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from typing import TYPE_CHECKING

from .models import User

if TYPE_CHECKING:
    CustomUserAdminBase = BaseUserAdmin[User]
else:
    CustomUserAdminBase = BaseUserAdmin


@admin.register(User)
class CustomUserAdmin(CustomUserAdminBase):
    """
    Custom admin configuration for the User model.
    Inherits from a type-aware base class for mypy and a standard base class for runtime.
    """

    list_display = ("email", "username", "first_name", "last_name", "is_staff")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("email",)
