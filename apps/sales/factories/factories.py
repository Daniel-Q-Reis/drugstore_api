import factory
from django.contrib.auth import get_user_model
from apps.sales.models import Sale, SaleItem
from apps.products.factories.factories import StockItemFactory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall('set_password', 'test_123')


class SaleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sale

    customer_name = factory.Faker('name')
    customer_email = factory.Faker('email')
    customer_phone = factory.Faker('phone_number')
    total_amount = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    discount_amount = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    final_amount = factory.LazyAttribute(
        lambda obj: obj.total_amount - obj.discount_amount
    )
    created_by = factory.SubFactory(UserFactory)


class SaleItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SaleItem

    sale = factory.SubFactory(SaleFactory)
    stock_item = factory.SubFactory(StockItemFactory)
    quantity = factory.Faker('pyint', min_value=1, max_value=10)
    unit_price = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    discount_percentage = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True)
    total_price = factory.LazyAttribute(
        lambda obj: obj.unit_price * obj.quantity
    )