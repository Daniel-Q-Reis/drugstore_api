from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response


from .dtos import SaleCreateDTO
from .models import Sale
from .serializers import SaleCreateSerializer, SaleSerializer
from .services import create_sale


class SaleViewSet(viewsets.ModelViewSet):
    queryset = (
        Sale.objects.select_related("created_by")
        .prefetch_related("items__stock_item__product")
        .all()
        .order_by("-created_at")
    )
    serializer_class = SaleSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["created_by"]
    search_fields = ["customer_name", "customer_email", "customer_phone"]
    ordering_fields = ["created_at", "final_amount"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "create":
            return SaleCreateSerializer
        return SaleSerializer

    def perform_create(self, serializer):
        # This method is not used because we override the create method
        pass

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the DTO from the serializer
        sale_dto: SaleCreateDTO = serializer.create(serializer.validated_data)
        sale_dto.user = request.user

        try:
            # Create sale using service function with DTO
            sale = create_sale(sale_dto, request.user)

            # Serialize and return the created sale
            sale_serializer = SaleSerializer(sale)
            return Response(sale_serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(
                {"error": "An error occurred while creating the sale"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
