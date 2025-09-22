from decimal import Decimal
import pytest
from django.utils import timezone

from dateutil.relativedelta import relativedelta

from apps.products.models import Brand, Category, Product, StockItem


@pytest.mark.django_db
class TestProductModels:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
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

    def test_brand_str(self) -> None:
        assert str(self.brand) == "Test Brand"  # nosec B101

    def test_category_str(self) -> None:
        assert str(self.category) == "Test Category"  # nosec B101

    def test_product_str(self) -> None:
        assert str(self.product) == "Test Product (TEST001)"  # nosec B101

    def test_stock_item_str(self) -> None:
        stock_item = StockItem.objects.create(
            product=self.product,
            batch_number="BATCH001",
            quantity=100,
            cost_price=10.00,
            selling_price=15.00,
            expiration_date=timezone.now().date() + relativedelta(months=7),
        )
        assert str(stock_item) == "Test Product - BATCH001"  # nosec B101

    @pytest.mark.parametrize(
        "months_ahead,expected_discount,description",
        [
            (1, 35, "Expires in 1 month (35% discount)"),
            (3, 25, "Expires in 3 months (25% discount)"),
            (5, 15, "Expires in 5 months (15% discount)"),
            (7, 0, "Expires in 7 months (0% discount)"),
        ],
    )
    def test_discount_percentage(
        self, months_ahead: int, expected_discount: int, description: str
    ) -> None:
        expiration_date = timezone.now().date() + relativedelta(months=months_ahead)
        stock_item = StockItem.objects.create(
            product=self.product,
            batch_number=f"BATCH{months_ahead:03d}",
            quantity=100,
            cost_price=10.00,
            selling_price=15.00,
            expiration_date=expiration_date,
        )
        assert stock_item.discount_percentage == expected_discount  # nosec B101

    def test_discounted_price(self) -> None:
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
        assert stock_item.discounted_price == Decimal("9.75")  # nosec B101
