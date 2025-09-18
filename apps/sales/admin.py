from django.contrib import admin
from .models import Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'total_amount', 'final_amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('customer_name', 'customer_email', 'customer_phone')
    ordering = ('-created_at',)
    inlines = [SaleItemInline]


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'stock_item', 'quantity', 'unit_price', 'total_price')
    list_filter = ('sale__created_at',)
    search_fields = ('sale__customer_name', 'stock_item__product__name')