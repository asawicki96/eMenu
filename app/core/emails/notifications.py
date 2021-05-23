from abc import ABC, abstractmethod, abstractproperty
from dishes.models import Dish
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
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
        return 'emenu@gmail.com'

    @abstractmethod
    def get_recipients(self) -> list:
        pass


class RecentDishesEmailNotification(BaseEmailNotificationClass):

    def __init__(self):
        self._context = self.get_context()

    def get_subject(self) -> str:
        return "Aktualizacja karty w aplikacji eMenu."

    def get_plaintext_message(self) -> str:
        rendered = render_to_string('emails/recent_dishes_notification/notification.txt', self._context)
        return rendered
    

    def get_html_message(self) -> str:
        rendered = render_to_string('emails/recent_dishes_notification/notification.html', self._context)
        return rendered

    def get_recipients(self) -> list:
        return [user.email for user in get_user_model().objects.all()]

    @property
    def get_context(self) -> dict:

        if self._context == None:
            self._context = {"recent_dishes": Dish.get_recent_objs()}

        return self._context
        