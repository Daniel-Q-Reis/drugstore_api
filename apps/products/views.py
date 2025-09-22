from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Brand, Category, Product, StockItem
from .serializers import (
    BrandSerializer,
    CategorySerializer,
    ProductSerializer,
    StockItemSerializer,
)


class BrandViewSet(viewsets.ModelViewSet[Brand]):
    queryset = Brand.objects.all().order_by("name")
    serializer_class = BrandSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]


class CategoryViewSet(viewsets.ModelViewSet[Category]):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]


class ProductViewSet(viewsets.ModelViewSet[Product]):
    queryset = (
        Product.objects.select_related("brand", "category").all().order_by("name")
    )
    serializer_class = ProductSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["brand", "category"]
    search_fields = ["name", "sku", "description"]
    ordering_fields = ["name", "sku", "created_at"]
    ordering = ["name"]


class StockItemViewSet(viewsets.ModelViewSet[StockItem]):
    queryset = (
        StockItem.objects.select_related(
            "product", "product__brand", "product__category"
        )
        .all()
        .order_by("expiration_date")
    )
    serializer_class = StockItemSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["product", "product__brand", "product__category"]
    search_fields = ["product__name", "batch_number"]
    ordering_fields = ["expiration_date", "quantity", "created_at"]
    ordering = ["expiration_date"]
