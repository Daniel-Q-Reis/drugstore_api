from rest_framework import serializers
from .models import Sale, SaleItem
from apps.products.serializers import ProductSerializer


class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='stock_item.product.name', read_only=True)
    batch_number = serializers.CharField(source='stock_item.batch_number', read_only=True)
    
    class Meta:
        model = SaleItem
        fields = '__all__'
        read_only_fields = ('sale',)


class SaleItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ('stock_item', 'quantity')


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Sale
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by', 'total_amount', 'discount_amount', 'final_amount')


class SaleCreateSerializer(serializers.ModelSerializer):
    items = SaleItemCreateSerializer(many=True)
    
    class Meta:
        model = Sale
        fields = ('customer_name', 'customer_email', 'customer_phone', 'items')
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        # The actual creation will be handled in the view
        # This is just for validation
        return validated_data