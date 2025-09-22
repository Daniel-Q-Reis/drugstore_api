import pytest
from typing import Any


@pytest.fixture
def user() -> Any:
    from apps.sales.factories.factories import UserFactory

    return UserFactory()


@pytest.fixture
def brand() -> Any:
    from apps.products.factories.factories import BrandFactory

    return BrandFactory()


@pytest.fixture
def category() -> Any:
    from apps.products.factories.factories import CategoryFactory

    return CategoryFactory()


@pytest.fixture
def product(brand: Any, category: Any) -> Any:
    from apps.products.factories.factories import ProductFactory

    return ProductFactory(brand=brand, category=category)


@pytest.fixture
def stock_item(product: Any) -> Any:
    from apps.products.factories.factories import StockItemFactory

    return StockItemFactory(product=product)


@pytest.fixture
def sale(user: Any) -> Any:
    from apps.sales.factories.factories import SaleFactory

    return SaleFactory(created_by=user)


@pytest.fixture
def sale_item(sale: Any, stock_item: Any) -> Any:
    from apps.sales.factories.factories import SaleItemFactory

    return SaleItemFactory(sale=sale, stock_item=stock_item)
