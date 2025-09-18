from celery import shared_task
from celery.schedules import crontab
from .tasks import notify_expiring_products


# Run daily at 9:00 AM
@shared_task
def daily_expiring_products_check():
    """
    Check for expiring products once a day.
    """
    return notify_expiring_products()