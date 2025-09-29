from decimal import Decimal
from typing import Any, Dict, no_type_check

from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import HttpRequest, JsonResponse
from django.utils import timezone

from dateutil.relativedelta import relativedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.products.models import StockItem
from apps.products.services import get_expiring_products, get_low_stock_products
from apps.sales.models import Sale, SaleItem
from apps.sales.services import get_sales_report


@no_type_check
@staff_member_required
def dashboard_data(request: HttpRequest) -> JsonResponse:
    """
    Provides data for the admin dashboard, following best practices for monetary values.

    This view performs all calculations using Python's `Decimal` type for accuracy.
    Final `Decimal` values are converted to strings in the JSON payload to prevent
    any loss of precision during JavaScript parsing.
    """
    today = timezone.now().date()
    current_month_start = today.replace(day=1)
    thirty_days_ago = today - relativedelta(days=30)
    six_months_ago = current_month_start - relativedelta(months=5)

    # --- KPI Card Data (Calculated with Decimal) ---
    sales_today = Sale.objects.filter(created_at__date=today)
    sales_this_month = Sale.objects.filter(created_at__gte=current_month_start)

    revenue_today = sales_today.aggregate(total=Sum("final_amount"))[
        "total"
    ] or Decimal("0.00")
    revenue_this_month = sales_this_month.aggregate(total=Sum("final_amount"))[
        "total"
    ] or Decimal("0.00")
    sales_count_today = sales_today.count()
    new_customers_this_month = (
        Sale.objects.filter(created_at__gte=current_month_start)
        .values("customer_email")
        .distinct()
        .count()
    )

    # --- Chart Data (Calculated with Decimal) ---
    # Monthly sales
    monthly_sales_data = (
        Sale.objects.filter(created_at__gte=six_months_ago)
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total_revenue=Sum("final_amount"))
        .order_by("month")
    )
    sales_labels = [d["month"].strftime("%b %Y") for d in monthly_sales_data]
    sales_values = [d["total_revenue"] or Decimal("0.00") for d in monthly_sales_data]

    # Top 5 Products by Revenue
    items_last_30_days = SaleItem.objects.filter(
        sale__created_at__date__gte=thirty_days_ago
    )
    total_revenue_last_30_days = items_last_30_days.aggregate(total=Sum("total_price"))[
        "total"
    ] or Decimal("0.00")

    top_5_revenue = (
        items_last_30_days.select_related("stock_item__product")
        .values("stock_item__product__name")
        .annotate(total_revenue=Sum("total_price"))
        .order_by("-total_revenue")[:5]
    )

    top_5_revenue_list = list(top_5_revenue)
    top_5_revenue_sum = sum(
        item["total_revenue"] for item in top_5_revenue_list if item["total_revenue"]
    )
    others_revenue = total_revenue_last_30_days - top_5_revenue_sum

    revenue_labels = [item["stock_item__product__name"] for item in top_5_revenue_list]
    revenue_values = [
        item["total_revenue"] or Decimal("0.00") for item in top_5_revenue_list
    ]

    if others_revenue > 0:
        revenue_labels.append("Others")
        revenue_values.append(others_revenue)

    # Top 5 products by quantity
    top_products_quantity = (
        items_last_30_days.select_related("stock_item__product")
        .values("stock_item__product__name")
        .annotate(total_quantity=Sum("quantity"))
        .order_by("-total_quantity")[:5]
    )
    quantity_labels = [
        item["stock_item__product__name"] for item in top_products_quantity
    ]
    quantity_values = [item["total_quantity"] or 0 for item in top_products_quantity]

    # --- Prepare final data structure, converting all Decimals to strings ---
    data = {
        "kpi": {
            "revenue_today": str(revenue_today),
            "revenue_this_month": str(revenue_this_month),
            "sales_today": sales_count_today,
            "new_customers_this_month": new_customers_this_month,
        },
        "charts": {
            "monthly_sales": {
                "labels": sales_labels,
                "values": [str(v) for v in sales_values],
            },
            "top_products_revenue": {
                "labels": revenue_labels,
                "values": [str(v) for v in revenue_values],
                "total": str(total_revenue_last_30_days),
            },
            "top_products_quantity": {
                "labels": quantity_labels,
                "values": quantity_values,
            },
        },
    }
    return JsonResponse(data)


# --- Existing API views below, now refactored for precision ---


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def inventory_summary(request: HttpRequest) -> Response:
    """
    Get a summary of the current inventory status.
    """
    total_products = StockItem.objects.count()
    total_quantity = StockItem.objects.aggregate(total=Sum("quantity"))["total"] or 0

    low_stock_items = get_low_stock_products().count()
    expiring_items = get_expiring_products().count()

    return Response(
        {
            "total_products": total_products,
            "total_quantity": total_quantity,
            "low_stock_items": low_stock_items,
            "expiring_items": expiring_items,
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def sales_summary(request: HttpRequest) -> Response:
    """
    Get a summary of sales, defaulting to the last 30 days.
    """
    days = int(request.query_params.get("days", 30))  # type: ignore[attr-defined]
    start_date = timezone.now().date() - relativedelta(days=days)

    report = get_sales_report(start_date=start_date)

    return Response(report)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def inventory_value(request: HttpRequest) -> Response:
    """
    Calculate the total value of inventory based on cost and selling price.
    Results are cached for 1 hour to improve performance.
    """
    cache_key = "inventory_value"
    cached_result = cache.get(cache_key)

    if cached_result:
        return Response(cached_result)

    stock_items = StockItem.objects.all()

    total_cost_value = Decimal("0")
    total_selling_value = Decimal("0")

    # Use iterator() for memory efficiency on large datasets.
    for item in stock_items.iterator():
        total_cost_value += item.cost_price * item.quantity
        total_selling_value += item.selling_price * item.quantity

    # Convert final Decimal values to strings for the API response.
    result: Dict[str, Any] = {
        "total_cost_value": str(total_cost_value),
        "total_selling_value": str(total_selling_value),
        "potential_profit": str(total_selling_value - total_cost_value),
    }

    # Cache for 1 hour (3600 seconds).
    cache.set(cache_key, result, 3600)

    return Response(result)
