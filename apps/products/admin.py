from django.contrib import admin
from typing import TYPE_CHECKING

from .models import Brand, Category, Product, StockItem

if TYPE_CHECKING:
    BrandAdminBase = admin.ModelAdmin[Brand]
    CategoryAdminBase = admin.ModelAdmin[Category]
    ProductAdminBase = admin.ModelAdmin[Product]
    StockItemAdminBase = admin.ModelAdmin[StockItem]
else:
    BrandAdminBase = admin.ModelAdmin
    CategoryAdminBase = admin.ModelAdmin
    ProductAdminBase = admin.ModelAdmin
    StockItemAdminBase = admin.ModelAdmin


@admin.register(Brand)
class BrandAdmin(BrandAdminBase):
    """
    Admin configuration for the Brand model.
    Inherits from a type-aware base class for mypy and a standard base class for runtime.
    """

    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Category)
class CategoryAdmin(CategoryAdminBase):
    """
    Admin configuration for the Category model.
    Inherits from a type-aware base class for mypy and a standard base class for runtime.
    """

    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Product)
class ProductAdmin(ProductAdminBase):
    """
    Admin configuration for the Product model.
    Inherits from a type-aware base class for mypy and a standard base class for runtime.
    """

    list_display = ("name", "sku", "brand", "category", "created_at")
    list_filter = ("brand", "category")
    search_fields = ("name", "sku")
    ordering = ("name",)


@admin.register(StockItem)
class StockItemAdmin(StockItemAdminBase):
    """
    Admin configuration for the StockItem model.
    Inherits from a type-aware base class for mypy and a standard base class for runtime.
    """

    list_display = (
        "product",
        "batch_number",
        "quantity",
        "expiration_date",
        "discount_percentage",
    )
    list_filter = ("expiration_date", "product__brand", "product__category")
    search_fields = ("product__name", "batch_number")
    ordering = ("expiration_date",)
