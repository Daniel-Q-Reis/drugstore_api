from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import InventoryViewSet

app_name = "inventory"

router = DefaultRouter()
router.register(r"inventory", InventoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
