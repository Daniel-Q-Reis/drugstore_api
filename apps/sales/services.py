from datetime import date
from decimal import Decimal
from typing import Any, Dict, Optional

from django.db import transaction

from apps.products.models import StockItem
from apps.users.models import User

from .dtos import SaleCreateDTO
from .models import Sale, SaleItem


@transaction.atomic
def create_sale(sale_dto: SaleCreateDTO, user: Optional[User] = None) -> Sale:
    """
    Create a sale with multiple items, updating stock quantities.

    Args:
        sale_dto: Data transfer object containing sale information.
        user: The user creating the sale.

    Returns:
        The created sale object.

    Raises:
        ValueError: If stock is insufficient or data is invalid.
    """
    total_amount_gross = Decimal("0.00")
    total_discount_amount = Decimal("0.00")

    for item_dto in sale_dto.items:
        try:
            stock_item = StockItem.objects.select_for_update().get(
                id=item_dto.stock_item_id
            )
        except StockItem.DoesNotExist:
            raise ValueError(
                f"Stock item with id {item_dto.stock_item_id} does not exist"
            )

        if stock_item.quantity < item_dto.quantity:
            raise ValueError(f"Insufficient stock for {stock_item.product.name}")

        original_price = stock_item.selling_price
        discounted_price = stock_item.discounted_price

        item_gross_total = original_price * item_dto.quantity
        item_final_total = discounted_price * item_dto.quantity
        item_discount = item_gross_total - item_final_total

        item_dto.unit_price = discounted_price
        item_dto.total_price = item_final_total
        item_dto.discount_percentage = Decimal(str(stock_item.discount_percentage))

        total_amount_gross += item_gross_total
        total_discount_amount += item_discount

    final_amount = total_amount_gross - total_discount_amount

    sale = Sale.objects.create(
        customer_name=sale_dto.customer_name,
        customer_email=sale_dto.customer_email,
        customer_phone=sale_dto.customer_phone,
        total_amount=total_amount_gross,
        discount_amount=total_discount_amount,
        final_amount=final_amount,
        created_by=user,
    )

    sale_items_to_create = []
    for item_dto in sale_dto.items:
        stock_item = StockItem.objects.get(id=item_dto.stock_item_id)
        stock_item.quantity -= item_dto.quantity
        stock_item.save(update_fields=["quantity"])

        sale_item = SaleItem(
            sale=sale,
            stock_item=stock_item,
            quantity=item_dto.quantity,
            unit_price=item_dto.unit_price,
            discount_percentage=item_dto.discount_percentage,
            total_price=item_dto.total_price,
        )
        sale_items_to_create.append(sale_item)

    SaleItem.objects.bulk_create(sale_items_to_create)

    return sale


def get_sales_report(
    start_date: Optional[date] = None, end_date: Optional[date] = None
) -> Dict[str, Any]:
    """
    Generate a sales report for a given period.

    Args:
        start_date: Start date for the report.
        end_date: End date for the report.

    Returns:
        A dictionary containing sales report data.
    """
    sales = Sale.objects.all()

    if start_date:
        sales = sales.filter(created_at__date__gte=start_date)

    if end_date:
        sales = sales.filter(created_at__date__lte=end_date)

    total_sales = sales.count()
    total_revenue = sum(sale.final_amount for sale in sales if sale.final_amount)

    return {
        "total_sales": total_sales,
        "total_revenue": float(total_revenue),
        "average_sale_value": float(total_revenue / total_sales)
        if total_sales > 0
        else 0,
        "period_start": start_date,
        "period_end": end_date,
    }
