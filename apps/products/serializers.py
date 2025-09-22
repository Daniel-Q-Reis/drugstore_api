from rest_framework import serializers

from .models import Brand, Category, Product, StockItem


class BrandSerializer(serializers.ModelSerializer[Brand]):
    class Meta:
        model = Brand
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class CategorySerializer(serializers.ModelSerializer[Category]):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class ProductSerializer(serializers.ModelSerializer[Product]):
    brand_name = serializers.CharField(source="brand.name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class StockItemSerializer(serializers.ModelSerializer[StockItem]):
    product_name = serializers.CharField(source="product.name", read_only=True)
    brand_name = serializers.CharField(source="product.brand.name", read_only=True)
    category_name = serializers.CharField(
        source="product.category.name", read_only=True
    )
    discount_percentage = serializers.DecimalField(
        max_digits=5, decimal_places=2, read_only=True
    )
    discounted_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = StockItem
        fields = "__all__"
        read_only_fields = (
            "created_at",
            "updated_at",
            "discount_percentage",
            "discounted_price",
        )


class StockItemCreateSerializer(serializers.ModelSerializer[StockItem]):
    class Meta:
        model = StockItem
        fields = "__all__"
