import json
from typing import TYPE_CHECKING, Any, Dict, Optional

from django.contrib import admin
from django.db.models import Model
from django.http import HttpRequest

from apps.products.models import StockItem
from .models import Sale, SaleItem

if TYPE_CHECKING:
    SaleItemInlineBase = admin.TabularInline[Model, Sale]
    SaleAdminBase = admin.ModelAdmin[Sale]
else:
    SaleItemInlineBase = admin.TabularInline
    SaleAdminBase = admin.ModelAdmin


class SaleItemInline(SaleItemInlineBase):
    """
    Inline admin configuration for SaleItem.
    This allows managing sale items directly within the sale creation form.
    """

    model = SaleItem
    extra = 1

    def get_formset(self, request: Any, obj: Any = None, **kwargs: Any) -> Any:
        """
        Set form fields as readonly in the admin inline.
        This renders the <input> tag but makes it non-editable by the user,
        allowing our JavaScript to find and populate it.
        """
        formset = super().get_formset(request, obj, **kwargs)
        form = formset.form
        readonly_fields = ("unit_price", "discount_percentage", "total_price")
        for field_name in readonly_fields:
            if field_name in form.base_fields:
                form.base_fields[field_name].widget.attrs["readonly"] = True
                form.base_fields[field_name].widget.attrs[
                    "style"
                ] = "background-color: #333;"  # Optional: visual cue
        return formset


@admin.register(Sale)
class SaleAdmin(SaleAdminBase):
    """
    Admin configuration for the Sale model.
    """

    add_form_template = "admin/sales/sale/change_form.html"
    change_form_template = "admin/sales/sale/change_form.html"
    list_display = ("id", "customer_name", "total_amount", "final_amount", "created_at")
    list_filter = ("created_at",)
    search_fields = ("customer_name", "customer_email", "customer_phone")
    ordering = ("-created_at",)
    inlines = [SaleItemInline]

    def get_form(
        self,
        request: HttpRequest,
        obj: Optional[Sale] = None,
        change: bool = False,
        **kwargs: Any,
    ) -> Any:
        """
        Set the main total fields as readonly in the form.
        """
        form = super().get_form(request, obj, **kwargs)
        readonly_fields = (
            "total_amount",
            "discount_amount",
            "final_amount",
            "created_by",
        )
        for field_name in readonly_fields:
            if field_name in form.base_fields:
                form.base_fields[field_name].widget.attrs["readonly"] = True
                form.base_fields[field_name].widget.attrs[
                    "style"
                ] = "background-color: #333;"
        return form

    def _get_stock_data_json(self) -> str:
        """
        Helper method to fetch all available stock items and serialize them to a JSON string.
        The data includes price, discount, and available quantity for the frontend.
        """
        # Fetch only items that are in stock to avoid cluttering the data.
        stock_items = StockItem.objects.filter(quantity__gt=0)
        stock_items_data = {
            item.id: {
                # Convert Decimal to string to preserve precision in JSON.
                "selling_price": str(item.selling_price),
                "discount_percentage": item.discount_percentage,
                "quantity": item.quantity,
            }
            for item in stock_items
        }
        return json.dumps(stock_items_data)

    def add_view(
        self,
        request: HttpRequest,
        form_url: str = "",
        extra_context: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Overrides the default add view to inject stock item data into the template context.
        This makes the data available for our custom JavaScript.
        """
        extra_context = extra_context or {}
        extra_context["stock_items_json"] = self._get_stock_data_json()
        return super().add_view(request, form_url, extra_context=extra_context)

    def change_view(
        self,
        request: HttpRequest,
        object_id: str,
        form_url: str = "",
        extra_context: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Overrides the default change view to inject stock item data,
        ensuring the functionality works for both creating and editing sales.
        """
        extra_context = extra_context or {}
        extra_context["stock_items_json"] = self._get_stock_data_json()
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )
