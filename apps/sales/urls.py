from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SaleViewSet

app_name = 'sales'

router = DefaultRouter()
router.register(r'sales', SaleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]