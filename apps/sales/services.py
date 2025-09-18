from django.db import transaction
from django.utils import timezone
from .models import Sale, SaleItem
from apps.products.models import StockItem


@transaction.atomic
def create_sale(customer_data, items_data, user=None):
    """
    Create a sale with multiple items, updating stock quantities.
    
    Args:
        customer_data (dict): Customer information
        items_data (list): List of dictionaries with stock_item_id and quantity
        user (User): User creating the sale
        
    Returns:
        Sale: The created sale object
        
    Raises:
        ValueError: If stock is insufficient or data is invalid
        Exception: For any other database errors
    """
    # Calculate totals
    total_amount = 0
    discount_amount = 0
    
    # Validate stock availability and calculate prices
    for item_data in items_data:
        stock_item_id = item_data['stock_item_id']
        quantity = item_data['quantity']
        
        try:
            stock_item = StockItem.objects.select_for_update().get(id=stock_item_id)
        except StockItem.DoesNotExist:
            raise ValueError(f"Stock item with id {stock_item_id} does not exist")
            
        if stock_item.quantity < quantity:
            raise ValueError(f"Insufficient stock for {stock_item.product.name}")
            
        # Calculate item price with discount
        unit_price = stock_item.discounted_price
        item_total = unit_price * quantity
        discount = (stock_item.selling_price - unit_price) * quantity
        
        item_data['unit_price'] = unit_price
        item_data['total_price'] = item_total
        item_data['discount_percentage'] = stock_item.discount_percentage
        
        total_amount += item_total
        discount_amount += discount
    
    # Create the sale
    sale = Sale.objects.create(
        customer_name=customer_data.get('name', ''),
        customer_email=customer_data.get('email', ''),
        customer_phone=customer_data.get('phone', ''),
        total_amount=total_amount,
        discount_amount=discount_amount,
        final_amount=total_amount - discount_amount,
        created_by=user
    )
    
    # Create sale items and update stock
    sale_items = []
    for item_data in items_data:
        stock_item_id = item_data['stock_item_id']
        quantity = item_data['quantity']
        
        # Update stock quantity
        stock_item = StockItem.objects.select_for_update().get(id=stock_item_id)
        stock_item.quantity -= quantity
        stock_item.save(update_fields=['quantity'])
        
        # Create sale item
        sale_item = SaleItem(
            sale=sale,
            stock_item=stock_item,
            quantity=quantity,
            unit_price=item_data['unit_price'],
            discount_percentage=item_data['discount_percentage'],
            total_price=item_data['total_price']
        )
        sale_items.append(sale_item)
    
    # Bulk create all sale items
    SaleItem.objects.bulk_create(sale_items)
    
    return sale


def get_sales_report(start_date=None, end_date=None):
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
        'total_sales': total_sales,
        'total_revenue': float(total_revenue),
        'average_sale_value': float(total_revenue / total_sales) if total_sales > 0 else 0,
        'period_start': start_date,
        'period_end': end_date
    }