from rest_framework import serializers
from typing import Any, Dict
from .dtos import SaleCreateDTO, SaleItemDTO
from .models import Sale, SaleItem


class SaleItemSerializer(serializers.ModelSerializer[SaleItem]):
    product_name = serializers.CharField(
        source="stock_item.product.name", read_only=True
    )
    batch_number = serializers.CharField(
        source="stock_item.batch_number", read_only=True
    )

    class Meta:
        model = SaleItem
        fields = "__all__"
        read_only_fields = ("sale",)


class SaleItemCreateSerializer(serializers.ModelSerializer[SaleItem]):
    class Meta:
        model = SaleItem
        fields = ("stock_item", "quantity")


class SaleSerializer(serializers.ModelSerializer[Sale]):
    items = SaleItemSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(
        source="created_by.get_full_name", read_only=True
    )

    class Meta:
        model = Sale
        fields = "__all__"
        read_only_fields = (
            "created_at",
            "updated_at",
            "created_by",
            "total_amount",
            "discount_amount",
            "final_amount",
        )


class SaleCreateSerializer(serializers.ModelSerializer[Sale]):
    items = SaleItemCreateSerializer(many=True)

    class Meta:
        model = Sale
        fields = ("customer_name", "customer_email", "customer_phone", "items")

    def create(self, validated_data: Dict[str, Any]) -> Sale:
        # This method is not used because we override the create method in the view
        # Returning a dummy Sale object to satisfy the type checker
        return Sale()

    def to_dto(self, validated_data: Dict[str, Any]) -> SaleCreateDTO:
        """Convert validated data to SaleCreateDTO."""
        items_data = validated_data.pop("items")
        # Transform validated data into a SaleCreateDTO
        sale_items = [
            SaleItemDTO(
                stock_item_id=item["stock_item"].id,
                quantity=item["quantity"],
                unit_price=item[
                    "stock_item"
                ].selling_price,  # Will be recalculated in service
                total_price=item["stock_item"].selling_price
                * item["quantity"],  # Will be recalculated in service
                discount_percentage=item[
                    "stock_item"
                ].discount_percentage,  # Will be recalculated in service
            )
            for item in items_data
        ]

        return SaleCreateDTO(
            customer_name=validated_data["customer_name"],
            customer_email=validated_data["customer_email"],
            customer_phone=validated_data["customer_phone"],
            items=sale_items,
        )
