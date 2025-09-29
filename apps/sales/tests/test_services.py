from decimal import Decimal
from typing import Any, Dict, List

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from apps.products.models import Brand, Category, Product, StockItem
from apps.sales.dtos import SaleCreateDTO, SaleItemDTO
from apps.sales.models import Sale, SaleItem
from apps.sales.services import create_sale, get_sales_report

User = get_user_model()


class SaleServiceTest(TestCase):
    def setUp(self) -> None:
        """Set up the necessary objects for the test suite."""
        self.user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123",  # nosec B106
        )
        self.brand = Brand.objects.create(name="Test Brand")
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            brand=self.brand,
            category=self.category,
            sku="TEST001",
        )
        self.stock_item = StockItem.objects.create(
            product=self.product,
            batch_number="BATCH001",
            quantity=100,
            cost_price=Decimal("10.00"),
            selling_price=Decimal("15.00"),
            expiration_date=timezone.now().date(),
        )

    def _create_sale_dto(
        self, customer_data: Dict[str, Any], items_data: List[Dict[str, Any]]
    ) -> SaleCreateDTO:
        """
        Helper method to construct a SaleCreateDTO from raw test data.
        This centralizes the DTO creation logic, making tests cleaner.
        """
        sale_item_dtos = []
        for item_data in items_data:
            stock_item = StockItem.objects.get(id=item_data["stock_item_id"])
            sale_item_dtos.append(
                SaleItemDTO(
                    stock_item_id=item_data["stock_item_id"],
                    quantity=item_data["quantity"],
                    unit_price=stock_item.selling_price,
                    total_price=stock_item.selling_price * item_data["quantity"],
                    discount_percentage=Decimal(str(stock_item.discount_percentage)),
                )
            )
        return SaleCreateDTO(
            customer_name=customer_data["name"],
            customer_email=customer_data["email"],
            customer_phone=customer_data["phone"],
            items=sale_item_dtos,
        )

    def test_create_sale_success(self) -> None:
        """
        Test that a sale is created successfully with valid data.
        """
        customer_data = {
            "name": "Test Customer",
            "email": "customer@example.com",
            "phone": "1234567890",
        }
        items_data = [{"stock_item_id": self.stock_item.id, "quantity": 2}]
        sale_dto = self._create_sale_dto(customer_data, items_data)

        sale = create_sale(sale_dto, self.user)

        # The stock item expires today, so it should have a 35% discount
        # Original price: 15.00 * 2 = 30.00
        # Discount: 35% of 30.00 = 10.50
        # Final amount: 30.00 - 10.50 = 19.50

        self.assertEqual(sale.customer_name, "Test Customer")
        self.assertEqual(sale.total_amount, Decimal("30.00"))
        self.assertEqual(sale.discount_amount, Decimal("10.50"))
        self.assertEqual(sale.final_amount, Decimal("19.50"))
        self.assertEqual(sale.created_by, self.user)

        sale_items = SaleItem.objects.filter(sale=sale)
        self.assertEqual(sale_items.count(), 1)

        sale_item = sale_items.first()
        assert sale_item is not None  # nosec B101
        self.assertEqual(sale_item.quantity, 2)
        # Unit price should be discounted: 15.00 - (15.00 * 0.35) = 9.75
        self.assertEqual(sale_item.unit_price, Decimal("9.75"))
        # Total price should be discounted: 9.75 * 2 = 19.50
        self.assertEqual(sale_item.total_price, Decimal("19.50"))

        self.stock_item.refresh_from_db()
        self.assertEqual(self.stock_item.quantity, 98)

    def test_create_sale_insufficient_stock(self) -> None:
        """
        Test that creating a sale fails if there is insufficient stock.
        """
        customer_data = {
            "name": "Test Customer",
            "email": "customer@example.com",
            "phone": "1234567890",
        }
        items_data = [{"stock_item_id": self.stock_item.id, "quantity": 150}]
        sale_dto = self._create_sale_dto(customer_data, items_data)

        with self.assertRaises(ValueError) as context:
            create_sale(sale_dto, self.user)
        self.assertIn("Insufficient stock", str(context.exception))

        self.assertEqual(Sale.objects.count(), 0)
        self.assertEqual(SaleItem.objects.count(), 0)

        self.stock_item.refresh_from_db()
        self.assertEqual(self.stock_item.quantity, 100)

    def test_create_sale_with_discount(self) -> None:
        """
        Test that a sale correctly applies discounts for expiring items.
        """
        expiring_stock_item = StockItem.objects.create(
            product=self.product,
            batch_number="BATCH002",
            quantity=50,
            cost_price=Decimal("10.00"),
            selling_price=Decimal("20.00"),
            expiration_date=timezone.now().date(),
        )
        customer_data = {
            "name": "Test Customer",
            "email": "customer@example.com",
            "phone": "1234567890",
        }
        items_data = [{"stock_item_id": expiring_stock_item.id, "quantity": 2}]
        sale_dto = self._create_sale_dto(customer_data, items_data)

        sale = create_sale(sale_dto, self.user)

        self.assertEqual(sale.total_amount, Decimal("40.00"))
        self.assertEqual(sale.discount_amount, Decimal("14.00"))
        self.assertEqual(sale.final_amount, Decimal("26.00"))

        sale_item = SaleItem.objects.get(sale=sale)
        self.assertEqual(sale_item.unit_price, Decimal("13.00"))
        self.assertEqual(sale_item.discount_percentage, Decimal("35.00"))
        self.assertEqual(sale_item.total_price, Decimal("26.00"))

    def test_get_sales_report(self) -> None:
        """
        Test the sales report generation service.
        """
        customer_data = {
            "name": "Test Customer",
            "email": "customer@example.com",
            "phone": "1234567890",
        }
        items_data = [{"stock_item_id": self.stock_item.id, "quantity": 2}]
        sale_dto = self._create_sale_dto(customer_data, items_data)

        self.stock_item.quantity = 100
        self.stock_item.save()

        create_sale(sale_dto, self.user)
        create_sale(sale_dto, self.user)

        report = get_sales_report()

        # Each sale has 2 items at 15.00 each = 30.00 total
        # With 35% discount = 10.50 discount
        # Final amount per sale = 19.50
        # Total revenue for 2 sales = 39.00
        # Average sale value = 19.50

        self.assertEqual(report["total_sales"], 2)
        self.assertEqual(report["total_revenue"], "39.00")
        self.assertEqual(report["average_sale_value"], "19.50")
