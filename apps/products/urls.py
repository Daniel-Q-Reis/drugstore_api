from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import BrandViewSet, CategoryViewSet, ProductViewSet, StockItemViewSet

app_name = "products"

router = DefaultRouter()
router.register(r"brands", BrandViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"products", ProductViewSet)
router.register(r"stock-items", StockItemViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
