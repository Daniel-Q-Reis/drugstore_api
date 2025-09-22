from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from typing import Any, Optional, Type, Union, cast

from .models import Sale
from .serializers import SaleCreateSerializer, SaleSerializer
from .services import create_sale
from apps.users.models import User


class SaleViewSet(viewsets.ModelViewSet[Sale]):
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

    def get_serializer_class(self) -> Type[Union[SaleCreateSerializer, SaleSerializer]]:
        if self.action == "create":
            return SaleCreateSerializer
        return SaleSerializer

    def perform_create(self, serializer: Any) -> None:
        # This method is not used because we override the create method
        pass

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Convert validated data to DTO
        sale_create_serializer = cast(SaleCreateSerializer, serializer)
        sale_dto = sale_create_serializer.to_dto(serializer.validated_data)

        # Handle the user type correctly
        user: Optional[User] = None
        if isinstance(request.user, User):
            user = request.user
            # We need to set the user on the DTO, but we can't do it directly
            # because of the type mismatch. We'll handle it in the service.

        try:
            # Create sale using service function with DTO
            sale = create_sale(sale_dto, user)

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
