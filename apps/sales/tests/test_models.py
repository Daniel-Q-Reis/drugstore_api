from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.products.models import Brand, Category, Product, StockItem
from apps.sales.models import Sale, SaleItem


class SaleModelTest(TestCase):
    def setUp(self) -> None:
        User = get_user_model()
        self.user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123",  # nosec B106
        )

        self.brand = Brand.objects.create(
            name="Test Brand", description="Test brand description"
        )

        self.category = Category.objects.create(
            name="Test Category", description="Test category description"
        )

        self.product = Product.objects.create(
            name="Test Product",
            description="Test product description",
            brand=self.brand,
            category=self.category,
            sku="TEST001",
        )

        self.stock_item = StockItem.objects.create(
            product=self.product,
            batch_number="BATCH001",
            quantity=100,
            cost_price=10.00,
            selling_price=15.00,
            expiration_date="2025-12-31",
        )

    def test_sale_str(self) -> None:
        sale = Sale.objects.create(
            customer_name="Test Customer",
            total_amount=30.00,
            discount_amount=0.00,
            final_amount=30.00,
            created_by=self.user,
        )
        self.assertEqual(str(sale), f"Sale #{sale.id} - Test Customer")

    def test_sale_item_str(self) -> None:
        sale = Sale.objects.create(
            customer_name="Test Customer",
            total_amount=30.00,
            discount_amount=0.00,
            final_amount=30.00,
            created_by=self.user,
        )

        sale_item = SaleItem.objects.create(
            sale=sale,
            stock_item=self.stock_item,
            quantity=2,
            unit_price=15.00,
            total_price=30.00,
        )
        self.assertEqual(str(sale_item), f"{self.product.name} x 2")
