from django.test import TestCase
from django.utils import timezone

from dateutil.relativedelta import relativedelta

from apps.products.models import Brand, Category, Product, StockItem
from apps.products.services import get_expiring_products, get_low_stock_products


class ProductServiceTest(TestCase):
    def setUp(self) -> None:
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

        # Create stock items for testing
        self.expiring_stock = StockItem.objects.create(
            product=self.product,
            batch_number="BATCH001",
            quantity=50,
            cost_price=10.00,
            selling_price=15.00,
            expiration_date=timezone.now().date()
            + relativedelta(days=15),  # Expires in 15 days
        )

        self.non_expiring_stock = StockItem.objects.create(
            product=self.product,
            batch_number="BATCH002",
            quantity=100,
            cost_price=10.00,
            selling_price=15.00,
            expiration_date=timezone.now().date()
            + relativedelta(days=120),  # Expires in 120 days
        )

        self.expired_stock = StockItem.objects.create(
            product=self.product,
            batch_number="BATCH003",
            quantity=30,
            cost_price=10.00,
            selling_price=15.00,
            expiration_date=timezone.now().date()
            - relativedelta(days=5),  # Expired 5 days ago
        )

        self.low_stock = StockItem.objects.create(
            product=self.product,
            batch_number="BATCH004",
            quantity=5,  # Below threshold of 10
            cost_price=10.00,
            selling_price=15.00,
            expiration_date=timezone.now().date() + relativedelta(days=120),
        )

        self.normal_stock = StockItem.objects.create(
            product=self.product,
            batch_number="BATCH004",
            quantity=25,  # Above threshold of 10
            cost_price=10.00,
            selling_price=15.00,
            expiration_date=timezone.now().date() + relativedelta(days=120),
        )

    def test_get_expiring_products(self) -> None:
        # Get products expiring within 30 days
        expiring_products = get_expiring_products(30)

        # Should include the expiring stock item
        self.assertIn(self.expiring_stock, expiring_products)

        # Should not include the non-expiring stock item
        self.assertNotIn(self.non_expiring_stock, expiring_products)

        # Should not include expired items
        expired_stock = StockItem.objects.create(
            product=self.product,
            batch_number="BATCH005",
            quantity=20,
            cost_price=10.00,
            selling_price=15.00,
            expiration_date=timezone.now().date()
            - relativedelta(days=5),  # Already expired
        )
        expiring_products = get_expiring_products(30)
        self.assertNotIn(expired_stock, expiring_products)

    def test_get_low_stock_products(self) -> None:
        # Get products with stock below threshold of 10
        low_stock_products = get_low_stock_products(10)

        # Should include the low stock item
        self.assertIn(self.low_stock, low_stock_products)

        # Should not include the normal stock item
        self.assertNotIn(self.normal_stock, low_stock_products)
