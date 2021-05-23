from django.test import TestCase
from unittest.mock import patch, Mock
from django.core.mail import EmailMultiAlternatives

from core.emails.notifications import RecentDishesEmailNotification
from core.emails.notification_service import EmailNotificationService


def pass_side_effect():
    pass

class TestRecentDishesEmailNotification(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.notification = RecentDishesEmailNotification()

class TestRecentDishesEmailNotification(TestCase):

    def setUp(self):
        self.notification = EmailNotificationService
        self.mock_context = {
            "subject" : "subject",
            "email_plaintext_message" : "plaintext message",
            "email_html_message" : "email html message",
            "from_mail" : "frommail",
            "recipients" : ["mail1", "mail2"]
        }

    def test_validate_success(self):
        result = EmailNotificationService._validate(self.mock_context)

        self.assertTrue(result)

    def test_validation_failure(self):
        mock_invalid_context = {
            "subject" : "",
            "email_plaintext_message" : "plaintext message",
            "email_html_message" : "email html message",
            "from_mail" : "frommail",
            "recipients" : [""]
        }
        result = EmailNotificationService._validate(mock_invalid_context)

        self.assertFalse(result)

    @patch.object(EmailNotificationService, '_validate')
    @patch.object(EmailNotificationService, '_get_context')
    @patch.object(EmailMultiAlternatives, 'send')
    def test_send_notification_returns_true_if_context_is_valid(self, send_mock, get_context_mock, validate_mock):

        send_mock.side_effect = pass_side_effect
        get_context_mock.return_value = self.mock_context

        validate_mock.return_value = True
        notification_mock = Mock()
        
        result = EmailNotificationService.send_notification(notification_mock)

        send_mock.assert_called()
        self.assertTrue(result)
        

    @patch.object(EmailNotificationService, '_validate')
    @patch.object(EmailNotificationService, '_get_context')
    @patch.object(EmailMultiAlternatives, 'send')
    def test_send_notification_returns_false_if_context_is_valid(self, send_mock, get_context_mock, validate_mock):

        send_mock.side_effect = pass_side_effect

        get_context_mock.return_value = {}
        validate_mock.return_value = False

        notification_mock = Mock()
        
        result = EmailNotificationService.send_notification(notification_mock)

        send_mock.assert_not_called()
        self.assertFalse(result)


    