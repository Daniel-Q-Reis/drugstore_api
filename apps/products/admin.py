from django.contrib import admin

from .models import Brand, Category, Product, StockItem


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "brand", "category", "created_at")
    list_filter = ("brand", "category")
    search_fields = ("name", "sku")
    ordering = ("name",)


@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
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
