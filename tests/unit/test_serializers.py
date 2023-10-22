import unittest
from unittest.mock import patch

from src.core.exceptions import InvalidEventTypeException, \
    MessageBodyIsInvalidException, InvalidEmailException
from src.infrastructure.serializers import EventSerializer
from src.core.entities import EventEntity


class TestSerializers(unittest.TestCase):

    @patch("src.infrastructure.serializers.LoggerServiceProvider")
    def setUp(self, mock_logger) -> None:
        self.event_serializer = EventSerializer(mock_logger)

    def tearDown(self) -> None:
        del self.event_serializer

    def test_serialize(self):
        self.assertEqual(self.event_serializer.serialize(
            EventEntity(
                event_type="new_publication",
                body="Hi.",
                to=None)
        ),
            {"event_type": "new_publication",
             "body": "Hi.",
             "to": None})

        self.assertEqual(self.event_serializer.serialize(
            EventEntity(
                event_type="approved_publication",
                body="This is a Test message.",
                to="ang@gmail.com")
        ),
            {"event_type": "approved_publication",
             "body": "This is a Test message.",
             "to": "ang@gmail.com"})

        self.assertEqual(self.event_serializer.serialize(
            EventEntity(
                event_type="new_publication",
                body="Hello.",
                to="davit@gmail")
        ),
            {"event_type": "new_publication",
             "body": "Hello.",
             "to": "davit@gmail"})

    def test_serializer_InvalidEventTypeException(self):
        self.assertRaises(InvalidEventTypeException,
                          self.event_serializer.serialize,
                          EventEntity(event_type="_publication",
                                      body="Hi.", to="angela@yahoo.com"))

    def test_serializer_MessageBodyIsInvalidException(self):
        self.assertRaises(MessageBodyIsInvalidException,
                          self.event_serializer.serialize,
                          EventEntity(event_type="new_publication",
                                      body="", to="angela@gmail.com"))

    def test_serializer_InvalidEmailException(self):
        self.assertRaises(InvalidEmailException,
                          self.event_serializer.serialize,
                          EventEntity(event_type="approved_publication",
                                      body="Hi.", to=None))

    def test_serializer_Exception(self):
        self.assertRaises(Exception, self.event_serializer.serialize,
                          EventEntity(event_type="approved_publication",
                                      body={"msg": "Hi."}, to="a@yahoo.com"))

    def test_deserialize(self):
        self.assertEqual(self.event_serializer.deserialize(
            {"event_type": "new_publication",
             "body": "Hi.",
             "to": None}
        ),
            EventEntity(
                event_type="new_publication",
                body="Hi.",
                to=None)
        )
        self.assertEqual(self.event_serializer.deserialize(
            {"event_type": "approved_publication",
             "body": "Test message.",
             "to": "anzhela.iondem@gmail.com"}
        ),
            EventEntity(
                event_type="approved_publication",
                body="Test message.",
                to="anzhela.iondem@gmail.com")
        )
        self.assertEqual(self.event_serializer.deserialize(
            {"event_type": "new_publication",
             "body": "Hi.",
             "to": "anzhela@gmail"}
        ),
            EventEntity(
                event_type="new_publication",
                body="Hi.",
                to="anzhela@gmail"
            )
        )

    def test_deserializer_InvalidEventTypeException(self):
        self.assertRaises(InvalidEventTypeException,
                          self.event_serializer.deserialize,
                          {"event_type": "_publication",
                           "body": "Hi.", "to": "angela@gmail.com"})

    def test_deserializer_MessageBodyIsInvalidException(self):
        self.assertRaises(MessageBodyIsInvalidException,
                          self.event_serializer.deserialize,
                          {"event_type": "new_publication",
                           "body": "", "to": "anna@yahoo.com"})

    def test_deserializer_InvalidEmailException(self):
        self.assertRaises(InvalidEmailException,
                          self.event_serializer.deserialize,
                          {"event_type": "approved_publication",
                           "body": "Hi.", "to": None})

    def test_deserializer_Exception(self):
        self.assertRaises(Exception, self.event_serializer.deserialize,
                          {"event_type": "approved_publication",
                           "body": {"msg": "Hi."}, "to": "a@yahoo.com"})
