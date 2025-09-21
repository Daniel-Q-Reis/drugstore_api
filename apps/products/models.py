from decimal import Decimal

from django.db import models
from django.utils import timezone


class Brand(models.Model):
    """
    Brand model for product manufacturers.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    """
    Category model for product classification.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    """
    Product model for items sold in the pharmacy.
    """

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_index=True)
    sku = models.CharField(max_length=50, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["brand"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.sku})"


class StockItem(models.Model):
    """
    StockItem model for tracking inventory.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    batch_number = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["expiration_date"]
        indexes = [
            models.Index(fields=["product"]),
            models.Index(fields=["batch_number"]),
            models.Index(fields=["expiration_date"]),
        ]

    def __str__(self) -> str:
        return f"{self.product.name} - {self.batch_number}"

    @property
    def discount_percentage(self) -> int:
        """
        Calculate discount percentage based on expiration date.
        35% if expires in 2 months or less
        25% if expires in 3-4 months
        15% if expires in 5-6 months
        0% otherwise
        """
        today = timezone.now().date()
        diff = self.expiration_date - today
        diff_days = diff.days

        if diff_days <= 60:  # 2 months
            return 35
        elif diff_days <= 120:  # 4 months
            return 25
        elif diff_days <= 180:  # 6 months
            return 15
        else:
            return 0

    @property
    def discounted_price(self) -> Decimal:
        """
        Calculate the discounted price based on discount percentage.
        """
        discount = Decimal(self.selling_price) * (
            Decimal(self.discount_percentage) / Decimal(100)
        )
        return Decimal(self.selling_price) - discount
