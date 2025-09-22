import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pharmacy_api.settings.development")

app = Celery("pharmacy_api")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Periodic tasks configuration
app.conf.beat_schedule = {
    "daily-expiring-products-check": {
        "task": "apps.products.tasks.daily_expiring_products_check",
        "schedule": crontab(hour="9", minute="0"),  # Daily at 9:00 AM
    },
}
