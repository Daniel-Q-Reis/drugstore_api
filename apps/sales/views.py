from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Sale, SaleItem
from .serializers import SaleSerializer, SaleCreateSerializer
from .services import create_sale
from apps.products.models import StockItem


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.select_related('created_by').prefetch_related('items__stock_item__product').all().order_by('-created_at')
    serializer_class = SaleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['created_by']
    search_fields = ['customer_name', 'customer_email', 'customer_phone']
    ordering_fields = ['created_at', 'final_amount']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SaleCreateSerializer
        return SaleSerializer
    
    def perform_create(self, serializer):
        # This method is not used because we override the create method
        pass
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Extract data for service function
        customer_data = {
            'name': request.data.get('customer_name', ''),
            'email': request.data.get('customer_email', ''),
            'phone': request.data.get('customer_phone', ''),
        }
        
        items_data = []
        for item in request.data.get('items', []):
            items_data.append({
                'stock_item_id': item['stock_item'],
                'quantity': item['quantity']
            })
        
        try:
            # Create sale using service function
            sale = create_sale(customer_data, items_data, request.user)
            
            # Serialize and return the created sale
            sale_serializer = SaleSerializer(sale)
            return Response(sale_serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'An error occurred while creating the sale'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)