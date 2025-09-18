from decimal import Decimal
from django.db import models
from django.conf import settings
from apps.products.models import StockItem
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.contrib.auth.models import User


class Sale(models.Model):
    """Sale model for tracking customer purchases."""
    
    customer_name: str = models.CharField(max_length=200)
    customer_email: str = models.EmailField(blank=True)
    customer_phone: str = models.CharField(max_length=200, blank=True)
    total_amount: Decimal = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount: Decimal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    final_amount: Decimal = models.DecimalField(max_digits=10, decimal_places=2)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['customer_name']),
        ]

    def __str__(self) -> str:
        return f"Sale #{self.id} - {self.customer_name}"


class SaleItem(models.Model):
    """SaleItem model for tracking individual items in a sale."""
    
    sale: Sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    stock_item: StockItem = models.ForeignKey(StockItem, on_delete=models.CASCADE)
    quantity: int = models.PositiveIntegerField()
    unit_price: Decimal = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage: Decimal = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    total_price: Decimal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return f"{self.stock_item.product.name} x {self.quantity}"
