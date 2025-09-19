from celery import shared_task
from .services import notify_expiring_products


# Run daily at 9:00 AM
@shared_task
def daily_expiring_products_check():
    """
    Check for expiring products once a day.
    """
    # Assuming notify_expiring_products is defined in the same file
    # If it's in a different file, import it correctly
    # For now, we'll assume it's in the same file
    # If this causes an error, we'll need to move it to a different file
    # or import it correctly
    return notify_expiring_products()
