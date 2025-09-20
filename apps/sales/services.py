from typing import Optional, Dict, Any
from datetime import date
from decimal import Decimal
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
        sale_dto (SaleCreateDTO): Data transfer object containing sale information
        user (User, optional): User creating the sale

    Returns:
        Sale: The created sale object

    Raises:
        ValueError: If stock is insufficient or data is invalid
        Exception: For any other database errors
    """
    # Calculate totals
    total_amount: Decimal = Decimal("0.00")
    discount_amount: Decimal = Decimal("0.00")

    # Validate stock availability and calculate prices
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

        # Calculate item price with discount
        unit_price = stock_item.discounted_price
        item_total = unit_price * item_dto.quantity
        discount = (stock_item.selling_price - unit_price) * item_dto.quantity

        # Update the DTO with calculated values
        item_dto.unit_price = unit_price
        item_dto.total_price = item_total
        item_dto.discount_percentage = Decimal(str(stock_item.discount_percentage))

        total_amount += item_total
        discount_amount += discount

    # Create the sale
    sale = Sale.objects.create(
        customer_name=sale_dto.customer_name,
        customer_email=sale_dto.customer_email,
        customer_phone=sale_dto.customer_phone,
        total_amount=total_amount,
        discount_amount=discount_amount,
        final_amount=total_amount - discount_amount,
        created_by=user,
    )

    # Create sale items and update stock
    sale_items = []
    for item_dto in sale_dto.items:
        # Update stock quantity
        stock_item = StockItem.objects.select_for_update().get(
            id=item_dto.stock_item_id
        )
        stock_item.quantity -= item_dto.quantity
        stock_item.save(update_fields=["quantity"])

        # Create sale item
        sale_item = SaleItem(
            sale=sale,
            stock_item=stock_item,
            quantity=item_dto.quantity,
            unit_price=item_dto.unit_price,
            discount_percentage=item_dto.discount_percentage,
            total_price=item_dto.total_price,
        )
        sale_items.append(sale_item)

    # Bulk create all sale items
    SaleItem.objects.bulk_create(sale_items)

    return sale


def get_sales_report(
    start_date: Optional[date] = None, end_date: Optional[date] = None
) -> Dict[str, Any]:
    """
    Generate a sales report for a given period.

    Args:
        start_date (date): Start date for the report
        end_date (date): End date for the report

    Returns:
        dict: Sales report data
    """
    sales = Sale.objects.all()

    if start_date:
        sales = sales.filter(created_at__date__gte=start_date)

    if end_date:
        sales = sales.filter(created_at__date__lte=end_date)

    total_sales = sales.count()
    total_revenue = sum(sale.final_amount for sale in sales)

    return {
        "total_sales": total_sales,
        "total_revenue": float(total_revenue),
        "average_sale_value": float(total_revenue / total_sales)
        if total_sales > 0
        else 0,
        "period_start": start_date,
        "period_end": end_date,
    }
