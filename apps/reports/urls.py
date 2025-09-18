from django.urls import path
from .views import inventory_summary, sales_summary, inventory_value

app_name = 'reports'

urlpatterns = [
    path('inventory/summary/', inventory_summary, name='inventory-summary'),
    path('sales/summary/', sales_summary, name='sales-summary'),
    path('inventory/value/', inventory_value, name='inventory-value'),
]