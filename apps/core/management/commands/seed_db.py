import random

from django.core.management.base import BaseCommand
from django.utils import timezone

from dateutil.relativedelta import relativedelta
from faker import Faker

from apps.products.models import Brand, Category, Product, StockItem
from apps.sales.models import Sale, SaleItem
from apps.sales.services import create_sale


class Command(BaseCommand):
    help = "Seed the database with sample data"

    def add_arguments(self, parser):
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

    def handle(self, *args, **options):
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
        brands = []
        for i in range(options["brands"]):
            brand = Brand.objects.create(
                name=fake.company(), description=fake.text(max_nb_chars=200)
            )
            brands.append(brand)

        # Create categories
        self.stdout.write("Creating categories...")
        categories = []
        for i in range(options["categories"]):
            category = Category.objects.create(
                name=fake.word().capitalize() + " " + fake.word().capitalize(),
                description=fake.text(max_nb_chars=200),
            )
            categories.append(category)

        # Create products
        self.stdout.write("Creating products...")
        products = []
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
                cost_price=random.uniform(5.0, 100.0),
                selling_price=random.uniform(10.0, 150.0),
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
                create_sale(customer_data, items_data)
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
