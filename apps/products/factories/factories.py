import factory
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from apps.products.models import Brand, Category, Product, StockItem


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Sequence(lambda n: f"Brand {n}")
    description = factory.Faker('text', max_nb_chars=200)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")
    description = factory.Faker('text', max_nb_chars=200)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"Product {n}")
    description = factory.Faker('text', max_nb_chars=200)
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)
    sku = factory.Sequence(lambda n: f"SKU{n:06d}")


class StockItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StockItem

    product = factory.SubFactory(ProductFactory)
    batch_number = factory.Sequence(lambda n: f"BATCH{n:06d}")
    quantity = factory.Faker('pyint', min_value=1, max_value=1000)
    cost_price = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    selling_price = factory.LazyAttribute(lambda obj: obj.cost_price * 1.5)
    expiration_date = factory.LazyFunction(
        lambda: timezone.now().date() + relativedelta(months=6)
    )