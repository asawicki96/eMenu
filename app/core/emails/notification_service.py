from dishes.models import Dish
from django.core.mail import EmailMultiAlternatives
import logging

from core.emails.notifications import BaseEmailNotificationClass

logger = logging.getLogger(__name__)

class EmailNotificationService:

    @staticmethod
    def send_notification(notification: BaseEmailNotificationClass) -> bool:

        context = EmailNotificationService._get_context(notification)

        if not EmailNotificationService._validate(context):
            logger.debug(f"EmailNotification context validation failed. Sending email skipped. Corrupted data: {str(context)}")
            return False

        message = EmailNotificationService._get_message(
            context = context
        )

        message.send()

        return True
    
    def _get_context(notification: BaseEmailNotificationClass) -> dict:

        try:
            context = {
                "subject" : notification.get_subject(),
                "email_plaintext_message" : notification.get_plaintext_message(),
                "email_html_message" : notification.get_html_message(),
                "from_mail" : notification.get_from_mail(),
                "recipients" : notification.get_recipients()
            }

            return context

        except Exception as e:
            logger.error(e)
            return None

    def _validate(context: dict) -> bool:
        required_keys = ('subject', 'email_plaintext_message', 'email_html_message', 'from_mail' ,'recipients')

        if not context:
            return False
        
        for key in required_keys:
            
            if not key in context or context[key] == None or context[key] == "":
                return False
        
        if not context["recipients"]:
            return False

        for recipient in context["recipients"]:
            
            if not isinstance(recipient, str):
                return False

        return True

    def _get_message(context: dict) -> EmailMultiAlternatives:
        
        message = EmailMultiAlternatives(
            # title:
            context["subject"],
            # message:
            context["email_plaintext_message"],
            # from:
            context["from_mail"],
            # to:
            context["recipients"]
        )

        message.attach_alternative(context["email_html_message"], "text/html")

        return message

        
