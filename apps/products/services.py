from django.utils import timezone
from django.db.models.query import QuerySet
from django.db.models.manager import Manager

from dateutil.relativedelta import relativedelta

from .models import StockItem


def get_expiring_products(days: int = 30) -> QuerySet[StockItem, Manager[StockItem]]:
    """
    Get products that are expiring within the specified number of days.

    Args:
        days (int): Number of days to check for expiration

    Returns:
        QuerySet: Stock items expiring within the specified days
    """
    cutoff_date = timezone.now().date() + relativedelta(days=days)
    return StockItem.objects.filter(
        expiration_date__lte=cutoff_date, expiration_date__gte=timezone.now().date()
    ).select_related("product", "product__brand", "product__category")


def get_low_stock_products(
    threshold: int = 10,
) -> QuerySet[StockItem, Manager[StockItem]]:
    """
    Get products with stock below the specified threshold.

    Args:
        threshold (int): Minimum stock level

    Returns:
        QuerySet: Stock items with quantity below threshold
    """
    return StockItem.objects.filter(quantity__lte=threshold).select_related(
        "product", "product__brand", "product__category"
    )
