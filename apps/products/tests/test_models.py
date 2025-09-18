from django.test import TestCase
from django.utils import timezone

from dateutil.relativedelta import relativedelta

from apps.products.models import Brand, Category, Product, StockItem


class ProductModelTest(TestCase):
    def setUp(self):
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

    def test_brand_str(self):
        self.assertEqual(str(self.brand), "Test Brand")

    def test_category_str(self):
        self.assertEqual(str(self.category), "Test Category")

    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Product (TEST001)")

    def test_stock_item_str(self):
        stock_item = StockItem.objects.create(
            product=self.product,
            batch_number="BATCH001",
            quantity=100,
            cost_price=10.00,
            selling_price=15.00,
            expiration_date=timezone.now().date() + relativedelta(months=7),
        )
        self.assertEqual(str(stock_item), "Test Product - BATCH001")

    def test_discount_percentage_35(self):
        # Expires in 1 month
        expiration_date = timezone.now().date() + relativedelta(months=1)
        stock_item = StockItem.objects.create(
            product=self.product,
            batch_number="BATCH001",
            quantity=100,
            cost_price=10.00,
            selling_price=15.00,
            expiration_date=expiration_date,
        )
        self.assertEqual(stock_item.discount_percentage, 35)

    def test_discount_percentage_25(self):
        # Expires in 3 months
        expiration_date = timezone.now().date() + relativedelta(months=3)
        stock_item = StockItem.objects.create(
            product=self.product,
            batch_number="BATCH002",
            quantity=100,
            cost_price=10.00,
            selling_price=15.00,
            expiration_date=expiration_date,
        )
        self.assertEqual(stock_item.discount_percentage, 25)

    def test_discount_percentage_15(self):
        # Expires in 5 months
        expiration_date = timezone.now().date() + relativedelta(months=5)
        stock_item = StockItem.objects.create(
            product=self.product,
            batch_number="BATCH003",
            quantity=100,
            cost_price=10.00,
            selling_price=15.00,
            expiration_date=expiration_date,
        )
        self.assertEqual(stock_item.discount_percentage, 15)

    def test_discount_percentage_0(self):
        # Expires in 7 months
        expiration_date = timezone.now().date() + relativedelta(months=7)
        stock_item = StockItem.objects.create(
            product=self.product,
            batch_number="BATCH004",
            quantity=100,
            cost_price=10.00,
            selling_price=15.00,
            expiration_date=expiration_date,
        )
        self.assertEqual(stock_item.discount_percentage, 0)

    def test_discounted_price(self):
        # Expires in 1 month (35% discount)
        expiration_date = timezone.now().date() + relativedelta(months=1)
        stock_item = StockItem.objects.create(
            product=self.product,
            batch_number="BATCH005",
            quantity=100,
            cost_price=10.00,
            selling_price=15.00,
            expiration_date=expiration_date,
        )
        # 35% of 15.00 = 5.25, so discounted price = 15.00 - 5.25 = 9.75
        self.assertEqual(stock_item.discounted_price, 9.75)
