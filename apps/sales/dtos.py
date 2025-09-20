from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional
from django.contrib.auth.models import User


@dataclass
class SaleItemDTO:
    """Data Transfer Object for sale items."""

    stock_item_id: int
    quantity: int
    unit_price: Decimal
    total_price: Decimal
    discount_percentage: Decimal


@dataclass
class SaleCreateDTO:
    """Data Transfer Object for creating a sale."""

    customer_name: str
    customer_email: str
    customer_phone: str
    items: List[SaleItemDTO]
    user: Optional[User] = None
