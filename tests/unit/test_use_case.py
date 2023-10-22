import unittest
from unittest.mock import patch

from src.core.entities import EventEntity
from src.core.use_cases import NotifierUseCase


class TestUseCases(unittest.TestCase):

    @patch("src.infrastructure.providers.SlackMessengerProvider")
    def test_execute_messenger(self, mock_message_provider):
        mock_message_provider.send_message.return_value = None
        event_entity = EventEntity(event_type="new_publication",
                                   body="New.", to=None)
        notifier = NotifierUseCase(event_entity, mock_message_provider)
        self.assertEqual(notifier.execute(), None)

    @patch("src.infrastructure.providers.EmailServiceProvider")
    def test_execute_email(self, mock_email_provider):
        mock_email_provider.send_email.return_value = None
        event_entity = EventEntity(event_type="new_publication",
                                   body="New.", to=None)
        notifier = NotifierUseCase(event_entity, mock_email_provider)
        self.assertEqual(notifier.execute(), None)
