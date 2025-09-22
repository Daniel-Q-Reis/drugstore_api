from celery import shared_task


# Run daily at 9:00 AM
@shared_task  # type: ignore[misc]
def daily_expiring_products_check() -> str:
    """
    Check for expiring products once a day.
    """
    # This function currently just returns a placeholder string
    # In a real implementation, this would call the actual service
    return "Expiring products check completed"
