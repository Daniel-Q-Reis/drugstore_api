import pytest
from django.contrib.auth import get_user_model
from apps.products.factories.factories import BrandFactory, CategoryFactory, ProductFactory, StockItemFactory
from apps.sales.factories.factories import UserFactory, SaleFactory, SaleItemFactory


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def brand():
    return BrandFactory()


@pytest.fixture
def category():
    return CategoryFactory()


@pytest.fixture
def product(brand, category):
    return ProductFactory(brand=brand, category=category)


@pytest.fixture
def stock_item(product):
    return StockItemFactory(product=product)


@pytest.fixture
def sale(user):
    return SaleFactory(created_by=user)


@pytest.fixture
def sale_item(sale, stock_item):
    return SaleItemFactory(sale=sale, stock_item=stock_item)