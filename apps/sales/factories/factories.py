from django.contrib.auth import get_user_model
from typing import Any

import factory

from apps.products.factories.factories import StockItemFactory
from apps.sales.models import Sale, SaleItem

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):  # type: ignore[type-arg]
    class Meta:
        model = "apps.users.User"

    username: Any = factory.Sequence(lambda n: f"user{n}")
    email: Any = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password: Any = factory.PostGenerationMethodCall("set_password", "test_123")


class SaleFactory(factory.django.DjangoModelFactory[Sale]):
    class Meta:
        model = Sale

    customer_name: Any = factory.Faker("name")
    customer_email: Any = factory.Faker("email")
    customer_phone: Any = factory.Faker("phone_number")
    total_amount: Any = factory.Faker(
        "pydecimal", left_digits=5, right_digits=2, positive=True
    )
    discount_amount: Any = factory.Faker(
        "pydecimal", left_digits=3, right_digits=2, positive=True
    )
    final_amount: Any = factory.LazyAttribute(
        lambda obj: obj.total_amount - obj.discount_amount
    )
    created_by: Any = factory.SubFactory(UserFactory)


class SaleItemFactory(factory.django.DjangoModelFactory[SaleItem]):
    class Meta:
        model = SaleItem

    sale: Any = factory.SubFactory(SaleFactory)
    stock_item: Any = factory.SubFactory(StockItemFactory)
    quantity: Any = factory.Faker("pyint", min_value=1, max_value=10)
    unit_price: Any = factory.Faker(
        "pydecimal", left_digits=4, right_digits=2, positive=True
    )
    discount_percentage: Any = factory.Faker(
        "pydecimal", left_digits=2, right_digits=2, positive=True
    )
    total_price: Any = factory.LazyAttribute(lambda obj: obj.unit_price * obj.quantity)
