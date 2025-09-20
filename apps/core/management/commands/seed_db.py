import random
from typing import Any, List
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandParser
from django.utils import timezone
from django.contrib.auth import get_user_model

from dateutil.relativedelta import relativedelta
from faker import Faker

from apps.products.models import Brand, Category, Product, StockItem
from apps.sales.models import Sale, SaleItem
from apps.sales.services import create_sale
from apps.sales.dtos import SaleCreateDTO, SaleItemDTO

User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with sample data"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--brands", type=int, default=10, help="Number of brands to create"
        )
        parser.add_argument(
            "--categories", type=int, default=15, help="Number of categories to create"
        )
        parser.add_argument(
            "--products", type=int, default=50, help="Number of products to create"
        )
        parser.add_argument(
            "--stock-items",
            type=int,
            default=100,
            help="Number of stock items to create",
        )
        parser.add_argument(
            "--sales", type=int, default=30, help="Number of sales to create"
        )

    def handle(self, *args: Any, **options: Any) -> None:
        fake = Faker()

        # Clear existing data
        self.stdout.write("Clearing existing data...")
        SaleItem.objects.all().delete()
        Sale.objects.all().delete()
        StockItem.objects.all().delete()
        Product.objects.all().delete()
        Brand.objects.all().delete()
        Category.objects.all().delete()

        # Create brands
        self.stdout.write("Creating brands...")
        brands: List[Brand] = []
        for i in range(options["brands"]):
            brand = Brand.objects.create(
                name=fake.company(), description=fake.text(max_nb_chars=200)
            )
            brands.append(brand)

        # Create categories
        self.stdout.write("Creating categories...")
        categories: List[Category] = []
        for i in range(options["categories"]):
            category = Category.objects.create(
                name=fake.word().capitalize() + " " + fake.word().capitalize(),
                description=fake.text(max_nb_chars=200),
            )
            categories.append(category)

        # Create products
        self.stdout.write("Creating products...")
        products: List[Product] = []
        for i in range(options["products"]):
            product = Product.objects.create(
                name=fake.word().capitalize() + " " + fake.word().capitalize(),
                description=fake.text(max_nb_chars=200),
                brand=random.choice(brands),
                category=random.choice(categories),
                sku=fake.unique.ean13(),
            )
            products.append(product)

        # Create stock items
        self.stdout.write("Creating stock items...")
        for i in range(options["stock_items"]):
            # Generate expiration date within next 2 years
            expiration_date = timezone.now().date() + relativedelta(
                months=random.randint(1, 24)
            )

            stock_item = StockItem.objects.create(
                product=random.choice(products),
                batch_number=fake.unique.ean8(),
                quantity=random.randint(10, 1000),
                cost_price=Decimal(str(random.uniform(5.0, 100.0))),
                selling_price=Decimal(str(random.uniform(10.0, 150.0))),
                expiration_date=expiration_date,
            )

        # Create sales
        self.stdout.write("Creating sales...")
        stock_items = list(StockItem.objects.all())

        for i in range(options["sales"]):
            # Select random stock items for this sale
            num_items = random.randint(1, 5)
            selected_stock_items = random.sample(
                stock_items, min(num_items, len(stock_items))
            )

            customer_data = {
                "name": fake.name(),
                "email": fake.email(),
                "phone": fake.phone_number(),
            }

            items_data = []
            for stock_item in selected_stock_items:
                items_data.append(
                    {"stock_item_id": stock_item.id, "quantity": random.randint(1, 5)}
                )

            try:
                # Create SaleItemDTO objects
                sale_item_dtos: List[SaleItemDTO] = []
                for item_data in items_data:
                    # Fetch the stock item to get the selling price
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

                # Create the sale using the DTO
                create_sale(sale_dto, user=None)
            except ValueError as e:
                self.stdout.write(f"Warning: Could not create sale - {e}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded database with:\n"
                f"- {len(brands)} brands\n"
                f"- {len(categories)} categories\n"
                f"- {len(products)} products\n"
                f'- {options["stock_items"]} stock items\n'
                f"- {Sale.objects.count()} sales"
            )
        )
