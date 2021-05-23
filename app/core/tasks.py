from celery import shared_task
from core.emails.notification_service import EmailNotificationService
from core.emails.notifications import RecentDishesEmailNotification
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_recent_dishes_email_notification():
    notification = RecentDishesEmailNotification()
    context = notification.context["recent_dishes"]
    logger.error(context)
    if notification.context["recent_dishes"]:
        result = EmailNotificationService.send_notification(notification)
        
        if result:
            logger.info(notification.get_plaintext_message())
            return True
        
    return False
    
