from drf_spectacular.utils import extend_schema
from drf_spectacular.views import SpectacularAPIView


class CustomSpectacularAPIView(SpectacularAPIView):
    @extend_schema(exclude=True)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
