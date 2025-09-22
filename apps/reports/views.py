from typing import Any, Dict
from django.core.cache import cache
from django.db.models import Sum
from django.utils import timezone
from django.http import HttpRequest

from dateutil.relativedelta import relativedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from decimal import Decimal

from apps.products.models import StockItem
from apps.products.services import get_expiring_products, get_low_stock_products
from apps.sales.services import get_sales_report


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def inventory_summary(request: HttpRequest) -> Response:
    """Get a summary of the current inventory."""
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
    """Get a summary of sales."""
    # Get date range from query parameters or default to last 30 days
    days = int(request.query_params.get("days", 30))  # type: ignore[attr-defined]
    start_date = timezone.now().date() - relativedelta(days=days)

    report = get_sales_report(start_date=start_date)

    return Response(report)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def inventory_value(request: HttpRequest) -> Response:
    """Calculate the total value of inventory."""
    # Try to get cached result
    cache_key = "inventory_value"
    cached_result = cache.get(cache_key)

    if cached_result:
        return Response(cached_result)

    stock_items = StockItem.objects.all()

    total_cost_value: Decimal = Decimal("0")
    total_selling_value: Decimal = Decimal("0")

    for item in stock_items:
        total_cost_value += item.cost_price * item.quantity
        total_selling_value += item.selling_price * item.quantity

    result: Dict[str, Any] = {
        "total_cost_value": float(total_cost_value),
        "total_selling_value": float(total_selling_value),
        "potential_profit": float(total_selling_value - total_cost_value),
    }

    # Cache for 1 hour
    cache.set(cache_key, result, 3600)

    return Response(result)
