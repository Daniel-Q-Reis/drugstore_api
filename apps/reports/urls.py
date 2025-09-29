from django.urls import path

from .views import (
    dashboard_data,
    inventory_summary,
    inventory_value,
    sales_summary,
)

app_name = "reports"

urlpatterns = [
    path("dashboard-data/", dashboard_data, name="dashboard-data"),
    path("inventory/summary/", inventory_summary, name="inventory-summary"),
    path("sales/summary/", sales_summary, name="sales-summary"),
    path("inventory/value/", inventory_value, name="inventory-value"),
]
