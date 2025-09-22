from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import InventoryItem


class InventoryViewSet(ViewSet):
    """
    A simple ViewSet for inventory operations.

    Mypy and django-stubs will infer the type of the model
    from the 'queryset' attribute, providing type safety
    inside the methods of this class.
    """

    queryset = InventoryItem.objects.all()

    def list(self, request: Request) -> Response:
        """
        Handles listing inventory items.
        """
        # Because of 'queryset = InventoryItem.objects.all()',
        # mypy knows that 'self.queryset' is a QuerySet[InventoryItem].
        # Any operations on self.queryset will be type-checked.
        return Response({"message": "Inventory list"})

    def retrieve(self, request: Request, pk: int | None = None) -> Response:
        """
        Handles retrieving a single inventory item.
        """
        return Response({"message": f"Inventory item {pk}"})
