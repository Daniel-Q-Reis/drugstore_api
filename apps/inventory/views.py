from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .models import InventoryItem


class InventoryViewSet(ViewSet):
    """
    A simple ViewSet for inventory operations.
    """
    queryset = InventoryItem.objects.all()

    def list(self, request):
        return Response({"message": "Inventory list"})

    def retrieve(self, request, pk=None):
        return Response({"message": f"Inventory item {pk}"})