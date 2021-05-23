from abc import ABC, abstractmethod, abstractproperty
from dishes.models import Dish
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class BaseEmailNotificationClass(ABC):

    @abstractmethod
    def get_subject(self) -> str:
        pass

    @abstractmethod
    def get_plaintext_message(self) -> str:
        pass

    @abstractmethod
    def get_html_message(self) -> str:
        pass

    def get_from_mail(self) -> str:
        return settings.DEFAULT_FROM_MAIL

    @abstractmethod
    def get_recipients(self) -> list:
        pass


class RecentDishesEmailNotification(BaseEmailNotificationClass):

    def __init__(self):
        self._context = None

    def get_subject(self) -> str:
        return "Aktualizacja karty w aplikacji eMenu."

    def get_plaintext_message(self) -> str:
        rendered = render_to_string('emails/recent_dishes_notification/notification.txt', self.context)

        return rendered
    

    def get_html_message(self) -> str:
        rendered = render_to_string('emails/recent_dishes_notification/notification.html', self.context)
        return rendered

    def get_recipients(self) -> list:
        return [user.email for user in get_user_model().objects.all()]

    @property
    def context(self) -> dict:

        if not self._context:

            self._context = {"recent_dishes": Dish.get_recent_objs()}

        return self._context
        