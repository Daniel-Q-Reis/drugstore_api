import random
from datetime import timedelta
from decimal import Decimal
from typing import Any, List

from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from django.utils import timezone

from dateutil.relativedelta import relativedelta
from faker import Faker

from apps.products.models import Brand, Category, Product, StockItem
from apps.sales.dtos import SaleCreateDTO, SaleItemDTO
from apps.sales.models import Sale, SaleItem
from apps.sales.services import create_sale
from apps.users.models import User


class Command(BaseCommand):
    """
    Seeds the database with a large, realistic, and varied set of sample data.
    """

    help = "Seed the database with realistic and extensive sample data."

    def add_arguments(self, parser: CommandParser) -> None:
        """
        Add command arguments to control the volume of data to be created.
        """
        parser.add_argument(
            "--brands", type=int, default=20, help="Number of brands to create"
        )
        parser.add_argument(
            "--categories", type=int, default=20, help="Number of categories to create"
        )
        parser.add_argument(
            "--products", type=int, default=100, help="Number of products to create"
        )
        parser.add_argument(
            "--stock-items",
            type=int,
            default=200,
            help="Number of stock items per product to create",
        )
        parser.add_argument(
            "--sales", type=int, default=450, help="Number of sales to create"
        )

    def handle(self, *args: Any, **options: Any) -> None:
        fake = Faker("pt_BR")
        self.stdout.write(self.style.SUCCESS("Starting database seeding process..."))

        with transaction.atomic():
            self.stdout.write("Wiping existing data...")
            SaleItem.objects.all().delete()
            Sale.objects.all().delete()
            StockItem.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()
            Brand.objects.all().delete()

        self.stdout.write("Defining realistic data pools...")
        brand_names = [
            "PharmaCorp",
            "MedLife",
            "BioGen",
            "HealthPlus",
            "VitaWell",
            "Natura",
            "L'Oréal",
            "Nivea",
            "Johnson & Johnson",
            "Pampers",
            "Huggies",
            "Coca-Cola",
            "PepsiCo",
            "Nestlé",
            "Danone",
            "Red Bull",
            "Gillette",
            "Colgate",
            "Dove",
            "Rexona",
            "Bayer",
            "Pfizer",
            "Roche",
            "GSK",
        ]
        category_names = [
            "Analgesics",
            "Antibiotics",
            "Vitamins",
            "Antihistamines",
            "Moisturizers",
            "Sunscreens",
            "Cleansers",
            "Serums",
            "Diapers",
            "Wipes",
            "Baby Oil",
            "Infant Formula",
            "Sodas",
            "Energy Drinks",
            "Juices",
            "Water",
            "Cereal Bars",
            "Yogurts",
            "Deodorants",
            "Oral Care",
            "Hair Care",
            "Shaving",
        ]

        self.stdout.write("Creating brands and categories...")
        brands = [
            Brand.objects.create(name=name)
            for name in random.sample(  # nosec B311
                brand_names, min(len(brand_names), options["brands"])
            )
        ]
        categories = [
            Category.objects.create(name=name)
            for name in random.sample(  # nosec B311
                category_names, min(len(category_names), options["categories"])
            )
        ]

        self.stdout.write("Creating products and stock items...")
        products: List[Product] = []
        for _ in range(options["products"]):
            product = Product.objects.create(
                name=f"{fake.word().capitalize()} {fake.word().capitalize()}",
                brand=random.choice(brands),  # nosec B311
                category=random.choice(categories),  # nosec B311
                sku=fake.unique.ean13(),
            )
            products.append(product)
            for _ in range(
                random.randint(
                    1, options["stock_items"] // options["products"]
                )  # nosec B311
            ):
                expiration = timezone.now().date() + relativedelta(
                    months=random.randint(2, 24)  # nosec B311
                )
                cost = Decimal(str(round(random.uniform(2.5, 80.0), 2)))  # nosec B311
                StockItem.objects.create(
                    product=product,
                    batch_number=fake.unique.ean8(),
                    quantity=random.randint(50, 500),  # nosec B311
                    cost_price=cost,
                    selling_price=cost
                    * Decimal(str(round(random.uniform(1.4, 2.2), 2))),  # nosec B311
                    expiration_date=expiration,
                )

        self.stdout.write(f"Creating {options['sales']} historical sales data...")
        all_stock_items = list(StockItem.objects.all())
        user = User.objects.filter(is_superuser=True).first()

        if not all_stock_items:
            self.stdout.write(
                self.style.WARNING(
                    "No stock items available to create sales. Skipping."
                )
            )
        else:
            for i in range(options["sales"]):
                sale_date = timezone.now() - timedelta(
                    days=random.randint(0, 365)  # nosec B311
                )
                num_items = random.randint(1, 4)  # nosec B311
                sale_stock_items = random.sample(  # nosec B311
                    all_stock_items, min(num_items, len(all_stock_items))
                )

                sale_item_dtos = [
                    SaleItemDTO(
                        stock_item_id=item.id,
                        quantity=random.randint(1, 3),  # nosec B311
                        unit_price=Decimal(0),
                        total_price=Decimal(0),
                        discount_percentage=Decimal(0),
                    )
                    for item in sale_stock_items
                ]
                sale_dto = SaleCreateDTO(
                    customer_name=fake.name(),
                    customer_email=fake.unique.email(),
                    customer_phone=fake.phone_number(),
                    items=sale_item_dtos,
                )
                try:
                    with transaction.atomic():
                        sale = create_sale(sale_dto, user=user)
                        Sale.objects.filter(pk=sale.pk).update(created_at=sale_date)
                except ValueError as e:
                    self.stdout.write(self.style.WARNING(f"Skipped creating sale: {e}"))

        fake.unique.clear()
        self.stdout.write(self.style.SUCCESS("Database seeding complete!"))
        self.stdout.write(
            f"- Brands: {Brand.objects.count()} | "
            f"Categories: {Category.objects.count()} | "
            f"Products: {Product.objects.count()} | "
            f"Stock Items: {StockItem.objects.count()} | "
            f"Sales: {Sale.objects.count()}"
        )
