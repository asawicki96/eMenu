from celery import shared_task
from core.emails.notification_service import EmailNotificationService
from core.emails.notifications import RecentDishesEmailNotification

@shared_task
def send_recent_dishes_email_notification():
    notification = RecentDishesEmailNotification()

    if (notification.get_context()["recent_dishes"]):
        result = EmailNotificationService.send_notification(notification)

        return result
    
    