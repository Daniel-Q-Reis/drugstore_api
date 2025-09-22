from decimal import Decimal
from django.utils import timezone
from typing import Any

import factory
from dateutil.relativedelta import relativedelta

from apps.products.models import Brand, Category, Product, StockItem


class BrandFactory(factory.django.DjangoModelFactory[Brand]):
    class Meta:
        model = Brand

    name: Any = factory.Sequence(lambda n: f"Brand {n}")
    description: Any = factory.Faker("text", max_nb_chars=200)


class CategoryFactory(factory.django.DjangoModelFactory[Category]):
    class Meta:
        model = Category

    name: Any = factory.Sequence(lambda n: f"Category {n}")
    description: Any = factory.Faker("text", max_nb_chars=200)


class ProductFactory(factory.django.DjangoModelFactory[Product]):
    class Meta:
        model = Product

    name: Any = factory.Sequence(lambda n: f"Product {n}")
    description: Any = factory.Faker("text", max_nb_chars=200)
    brand: Any = factory.SubFactory(BrandFactory)
    category: Any = factory.SubFactory(CategoryFactory)
    sku: Any = factory.Sequence(lambda n: f"SKU{n:06d}")


class StockItemFactory(factory.django.DjangoModelFactory[StockItem]):
    class Meta:
        model = StockItem

    product: Any = factory.SubFactory(ProductFactory)
    batch_number: Any = factory.Sequence(lambda n: f"BATCH{n:06d}")
    quantity: Any = factory.Faker("pyint", min_value=1, max_value=1000)
    cost_price: Any = factory.Faker(
        "pydecimal", left_digits=4, right_digits=2, positive=True
    )
    selling_price: Any = factory.LazyAttribute(
        lambda obj: obj.cost_price * Decimal("1.5")
    )
    expiration_date: Any = factory.LazyFunction(
        lambda: timezone.now().date() + relativedelta(months=6)
    )
