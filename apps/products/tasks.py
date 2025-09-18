from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .services import get_expiring_products


@shared_task
def notify_expiring_products():
    """
    Notify about products that are expiring within 30 days.
    This is a placeholder task that would typically send emails or notifications.
    """
    expiring_products = get_expiring_products(30)
    
    if expiring_products.exists():
        # In a real application, you would send an email or notification here
        # For now, we'll just print to console
        print(f"Found {expiring_products.count()} products expiring within 30 days")
        
        # Example of what you might do in a real application:
        # subject = 'Expiring Products Alert'
        # message = f'The following products are expiring within 30 days:\n\n'
        # for item in expiring_products:
        #     message += f"- {item.product.name} (Batch: {item.batch_number}, Expiry: {item.expiration_date})\n"
        # 
        # send_mail(
        #     subject,
        #     message,
        #     settings.DEFAULT_FROM_EMAIL,
        #     ['manager@pharmacy.com'],
        #     fail_silently=False,
        # )
        
        return f"Notified about {expiring_products.count()} expiring products"
    
    return "No expiring products found"