from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import InventoryItem


class InventoryViewSet(ViewSet[InventoryItem]):
    """
    A simple ViewSet for inventory operations.
    """

    queryset = InventoryItem.objects.all()

    def list(self, request: Request) -> Response:
        return Response({"message": "Inventory list"})

    def retrieve(self, request: Request, pk: str | None = None) -> Response:
        return Response({"message": f"Inventory item {pk}"})
