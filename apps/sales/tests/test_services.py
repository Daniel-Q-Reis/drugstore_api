from decimal import Decimal
from typing import List, Dict, Any
from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.products.models import Brand, Category, Product, StockItem
from apps.sales.models import Sale, SaleItem
from apps.sales.services import create_sale, get_sales_report
from apps.sales.dtos import SaleCreateDTO, SaleItemDTO


class SaleServiceTest(TestCase):
    def setUp(self) -> None:
        User = get_user_model()
        self.user = User.objects.create_user(
            email="test@example.com", username="testuser", password="testpass123"
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
            cost_price=Decimal("10.00"),
            selling_price=Decimal("15.00"),
            expiration_date=date(2025, 12, 31),
        )

    def test_create_sale_success(self) -> None:
        customer_data: Dict[str, Any] = {
            "name": "Test Customer",
            "email": "customer@example.com",
            "phone": "1234567890",
        }

        items_data: List[Dict[str, Any]] = [
            {"stock_item_id": self.stock_item.id, "quantity": 2}
        ]

        # Create SaleItemDTO objects
        sale_item_dtos = []
        for item_data in items_data:
            stock_item = StockItem.objects.get(id=item_data["stock_item_id"])
            unit_price = stock_item.selling_price
            quantity = item_data["quantity"]
            total_price = unit_price * quantity
            discount_percentage = Decimal(str(stock_item.discount_percentage))

            sale_item_dto = SaleItemDTO(
                stock_item_id=item_data["stock_item_id"],
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price,
                discount_percentage=discount_percentage,
            )
            sale_item_dtos.append(sale_item_dto)

        # Create SaleCreateDTO object
        sale_dto = SaleCreateDTO(
            customer_name=customer_data["name"],
            customer_email=customer_data["email"],
            customer_phone=customer_data["phone"],
            items=sale_item_dtos,
        )

        sale = create_sale(sale_dto, self.user)

        # Check sale was created
        self.assertEqual(sale.customer_name, "Test Customer")
        self.assertEqual(sale.total_amount, Decimal("30.00"))
        self.assertEqual(sale.final_amount, Decimal("30.00"))
        self.assertEqual(sale.created_by, self.user)

        # Check sale item was created
        sale_items = SaleItem.objects.filter(sale=sale)
        self.assertEqual(sale_items.count(), 1)

        sale_item = sale_items.first()
        assert sale_item is not None  # Add assertion to satisfy mypy
        self.assertEqual(sale_item.quantity, 2)
        self.assertEqual(sale_item.unit_price, Decimal("15.00"))
        self.assertEqual(sale_item.total_price, Decimal("30.00"))

        # Check stock was updated
        self.stock_item.refresh_from_db()
        self.assertEqual(self.stock_item.quantity, 98)

    def test_create_sale_insufficient_stock(self) -> None:
        customer_data: Dict[str, Any] = {
            "name": "Test Customer",
            "email": "customer@example.com",
            "phone": "1234567890",
        }

        items_data: List[Dict[str, Any]] = [
            {
                "stock_item_id": self.stock_item.id,
                "quantity": 150,  # More than available stock
            }
        ]

        # Create SaleItemDTO objects
        sale_item_dtos = []
        for item_data in items_data:
            stock_item = StockItem.objects.get(id=item_data["stock_item_id"])
            unit_price = stock_item.selling_price
            quantity = item_data["quantity"]
            total_price = unit_price * quantity
            discount_percentage = Decimal(str(stock_item.discount_percentage))

            sale_item_dto = SaleItemDTO(
                stock_item_id=item_data["stock_item_id"],
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price,
                discount_percentage=discount_percentage,
            )
            sale_item_dtos.append(sale_item_dto)

        # Create SaleCreateDTO object
        sale_dto = SaleCreateDTO(
            customer_name=customer_data["name"],
            customer_email=customer_data["email"],
            customer_phone=customer_data["phone"],
            items=sale_item_dtos,
        )

        with self.assertRaises(ValueError) as context:
            create_sale(sale_dto, self.user)

        self.assertIn("Insufficient stock", str(context.exception))

        # Check no sale was created
        self.assertEqual(Sale.objects.count(), 0)

        # Check no sale items were created
        self.assertEqual(SaleItem.objects.count(), 0)

        # Check stock was not modified
        self.stock_item.refresh_from_db()
        self.assertEqual(self.stock_item.quantity, 100)

    def test_create_sale_with_discount(self) -> None:
        # Create a stock item that expires soon (35% discount)
        expiring_stock_item = StockItem.objects.create(
            product=self.product,
            batch_number="BATCH002",
            quantity=50,
            cost_price=Decimal("10.00"),
            selling_price=Decimal("20.00"),
            expiration_date=date(2023, 10, 1),  # Past expiration for discount
        )

        customer_data: Dict[str, Any] = {
            "name": "Test Customer",
            "email": "customer@example.com",
            "phone": "1234567890",
        }

        items_data: List[Dict[str, Any]] = [
            {"stock_item_id": expiring_stock_item.id, "quantity": 2}
        ]

        # Create SaleItemDTO objects
        sale_item_dtos = []
        for item_data in items_data:
            stock_item = StockItem.objects.get(id=item_data["stock_item_id"])
            unit_price = stock_item.selling_price
            quantity = item_data["quantity"]
            total_price = unit_price * quantity
            discount_percentage = Decimal(str(stock_item.discount_percentage))

            sale_item_dto = SaleItemDTO(
                stock_item_id=item_data["stock_item_id"],
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price,
                discount_percentage=discount_percentage,
            )
            sale_item_dtos.append(sale_item_dto)

        # Create SaleCreateDTO object
        sale_dto = SaleCreateDTO(
            customer_name=customer_data["name"],
            customer_email=customer_data["email"],
            customer_phone=customer_data["phone"],
            items=sale_item_dtos,
        )

        sale = create_sale(sale_dto, self.user)

        # Check sale was created with discount
        self.assertEqual(sale.total_amount, Decimal("40.00"))  # 2 * 20.00
        self.assertEqual(sale.discount_amount, Decimal("14.00"))  # 2 * (20.00 * 0.35)
        self.assertEqual(sale.final_amount, Decimal("26.00"))  # 40.00 - 14.00

        # Check sale item was created with discount
        sale_item = SaleItem.objects.get(sale=sale)
        self.assertEqual(
            sale_item.unit_price, Decimal("13.00")
        )  # 20.00 - (20.00 * 0.35)
        self.assertEqual(sale_item.discount_percentage, Decimal("35.00"))
        self.assertEqual(sale_item.total_price, Decimal("26.00"))

    def test_get_sales_report(self) -> None:
        # Create some sales
        customer_data: Dict[str, Any] = {
            "name": "Test Customer",
            "email": "customer@example.com",
            "phone": "1234567890",
        }

        items_data: List[Dict[str, Any]] = [
            {"stock_item_id": self.stock_item.id, "quantity": 2}
        ]

        # Create SaleItemDTO objects
        sale_item_dtos = []
        for item_data in items_data:
            stock_item = StockItem.objects.get(id=item_data["stock_item_id"])
            unit_price = stock_item.selling_price
            quantity = item_data["quantity"]
            total_price = unit_price * quantity
            discount_percentage = Decimal(str(stock_item.discount_percentage))

            sale_item_dto = SaleItemDTO(
                stock_item_id=item_data["stock_item_id"],
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price,
                discount_percentage=discount_percentage,
            )
            sale_item_dtos.append(sale_item_dto)

        # Create SaleCreateDTO object
        sale_dto = SaleCreateDTO(
            customer_name=customer_data["name"],
            customer_email=customer_data["email"],
            customer_phone=customer_data["phone"],
            items=sale_item_dtos,
        )

        # Create two sales
        create_sale(sale_dto, self.user)
        create_sale(sale_dto, self.user)

        # Get report
        report = get_sales_report()

        self.assertEqual(report["total_sales"], 2)
        self.assertEqual(report["total_revenue"], 60.0)  # 2 sales * 30.00 each
        self.assertEqual(report["average_sale_value"], 30.0)
