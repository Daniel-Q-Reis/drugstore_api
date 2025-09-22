import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from apps.products.factories.factories import (
    BrandFactory,
    CategoryFactory,
    ProductFactory,
    StockItemFactory,
)

from apps.users.models import User
from apps.products.models import Product, StockItem


@pytest.mark.django_db
class TestSaleViewSet:
    """Integration tests for the SaleViewSet."""

    @pytest.fixture
    def api_client(self) -> APIClient:
        """Create an API client for testing."""
        return APIClient()

    @pytest.fixture
    def user(self) -> User:
        """Create a test user."""
        return User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",  # nosec B106
        )

    @pytest.fixture
    def authenticated_client(self, api_client: APIClient, user: User) -> APIClient:
        """Create an authenticated API client."""
        api_client.force_authenticate(user=user)
        return api_client

    @pytest.fixture
    def product_data(self) -> tuple[Product, StockItem]:
        """Create test products and stock items."""
        brand = BrandFactory()
        category = CategoryFactory()
        product = ProductFactory(brand=brand, category=category)
        stock_item = StockItemFactory(product=product, quantity=100)
        return product, stock_item  # type: ignore[return-value]

    def test_create_sale_success(
        self, authenticated_client: APIClient, product_data: tuple[Product, StockItem]
    ) -> None:
        """Test successful sale creation."""
        product, stock_item = product_data

        url = reverse("sales:sale-list")
        data = {
            "customer_name": "John Doe",
            "customer_email": "john@example.com",
            "customer_phone": "+1234567890",
            "items": [{"stock_item": stock_item.id, "quantity": 2}],
        }

        response = authenticated_client.post(url, data, format="json")

        # Check that the response is successful
        assert response.status_code == status.HTTP_201_CREATED  # nosec B101

        # Check that the response contains the expected data
        assert response.data["customer_name"] == "John Doe"  # nosec B101
        assert response.data["customer_email"] == "john@example.com"  # nosec B101
        assert response.data["customer_phone"] == "+1234567890"  # nosec B101
        assert len(response.data["items"]) == 1  # nosec B101
        assert response.data["items"][0]["quantity"] == 2  # nosec B101

        # Check that the stock quantity was updated
        stock_item.refresh_from_db()
        assert stock_item.quantity == 98  # 100 - 2  # nosec B101

    def test_create_sale_insufficient_stock(
        self, authenticated_client: APIClient, product_data: tuple[Product, StockItem]
    ) -> None:
        """Test sale creation with insufficient stock."""
        product, stock_item = product_data

        url = reverse("sales:sale-list")
        data = {
            "customer_name": "John Doe",
            "customer_email": "john@example.com",
            "customer_phone": "+1234567890",
            "items": [
                {
                    "stock_item": stock_item.id,
                    "quantity": 150,  # More than available stock
                }
            ],
        }

        response = authenticated_client.post(url, data, format="json")

        # Check that the response is a bad request
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # nosec B101
        assert "error" in response.data  # nosec B101

        # Check that the stock quantity was not updated
        stock_item.refresh_from_db()
        assert stock_item.quantity == 100  # Unchanged  # nosec B101

    def test_create_sale_invalid_data(self, authenticated_client: APIClient) -> None:
        """Test sale creation with invalid data."""
        url = reverse("sales:sale-list")
        data = {
            "customer_name": "",  # Required field
            "customer_email": "invalid-email",  # Invalid email
            "items": [],  # Required field
        }

        response = authenticated_client.post(url, data, format="json")

        # Check that the response is a bad request
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # nosec B101

    def test_create_sale_unauthenticated(
        self, api_client: APIClient, product_data: tuple[Product, StockItem]
    ) -> None:
        """Test sale creation without authentication."""
        product, stock_item = product_data

        url = reverse("sales:sale-list")
        data = {
            "customer_name": "John Doe",
            "customer_email": "john@example.com",
            "customer_phone": "+1234567890",
            "items": [{"stock_item": stock_item.id, "quantity": 2}],
        }

        response = api_client.post(url, data, format="json")

        # Check that the response is unauthorized
        assert response.status_code == status.HTTP_401_UNAUTHORIZED  # nosec B101
