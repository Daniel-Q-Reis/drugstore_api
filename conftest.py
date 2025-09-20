import pytest

from apps.products.factories.factories import (
    BrandFactory,
    CategoryFactory,
    ProductFactory,
    StockItemFactory,
)
from apps.sales.factories.factories import SaleFactory, SaleItemFactory, UserFactory
from apps.users.models import User
from apps.products.models import Brand, Category, Product, StockItem
from apps.sales.models import Sale, SaleItem


@pytest.fixture
def user() -> User:
    return UserFactory()  # type: ignore[return-value]


@pytest.fixture
def brand() -> Brand:
    return BrandFactory()  # type: ignore[return-value]


@pytest.fixture
def category() -> Category:
    return CategoryFactory()  # type: ignore[return-value]


@pytest.fixture
def product(brand: Brand, category: Category) -> Product:
    return ProductFactory(brand=brand, category=category)  # type: ignore[return-value]


@pytest.fixture
def stock_item(product: Product) -> StockItem:
    return StockItemFactory(product=product)  # type: ignore[return-value]


@pytest.fixture
def sale(user: User) -> Sale:
    return SaleFactory(created_by=user)  # type: ignore[return-value]


@pytest.fixture
def sale_item(sale: Sale, stock_item: StockItem) -> SaleItem:
    return SaleItemFactory(sale=sale, stock_item=stock_item)  # type: ignore[return-value]
