from django.contrib import admin
from django.db.models import Model
from typing import TYPE_CHECKING

from .models import Sale, SaleItem

if TYPE_CHECKING:
    SaleItemInlineBase = admin.TabularInline[Model, Sale]
    SaleAdminBase = admin.ModelAdmin[Sale]
    SaleItemAdminBase = admin.ModelAdmin[SaleItem]
else:
    SaleItemInlineBase = admin.TabularInline
    SaleAdminBase = admin.ModelAdmin
    SaleItemAdminBase = admin.ModelAdmin


class SaleItemInline(SaleItemInlineBase):
    """
    Inline admin configuration for SaleItem within Sale admin.
    Inherits from a type-aware base class for mypy and a standard base class for runtime.
    """

    model = SaleItem
    extra = 1


@admin.register(Sale)
class SaleAdmin(SaleAdminBase):
    """
    Admin configuration for the Sale model.
    Inherits from a type-aware base class for mypy and a standard base class for runtime.
    """

    list_display = ("id", "customer_name", "total_amount", "final_amount", "created_at")
    list_filter = ("created_at",)
    search_fields = ("customer_name", "customer_email", "customer_phone")
    ordering = ("-created_at",)
    inlines = [SaleItemInline]


@admin.register(SaleItem)
class SaleItemAdmin(SaleItemAdminBase):
    """
    Admin configuration for the SaleItem model.
    Inherits from a type-aware base class for mypy and a standard base class for runtime.
    """

    list_display = ("sale", "stock_item", "quantity", "unit_price", "total_price")
    list_filter = ("sale__created_at",)
    search_fields = ("sale__customer_name", "stock_item__product__name")
