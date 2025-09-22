from typing import Any
from drf_spectacular.utils import extend_schema
from drf_spectacular.views import SpectacularAPIView
from rest_framework.request import Request
from rest_framework.response import Response


class CustomSpectacularAPIView(SpectacularAPIView):
    @extend_schema(exclude=True)
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)
