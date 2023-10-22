import unittest

import src.core.validators as scv
from src.core.exceptions import InvalidEmailException, \
    MessageBodyIsInvalidException, InvalidEventTypeException


class TestValidators(unittest.TestCase):

    def test_check_event_type(self):
        self.assertTrue(scv.check_event_type("approved_publication"))
        self.assertTrue(scv.check_event_type("new_publication"))
        self.assertRaises(InvalidEventTypeException, scv.check_event_type, "_p")
        self.assertRaises(InvalidEventTypeException, scv.check_event_type, "")

    def test_check_event_body(self):
        self.assertTrue(scv.check_event_body("Hi."))
        self.assertRaises(MessageBodyIsInvalidException,
                          scv.check_event_body, "")
        self.assertRaises(MessageBodyIsInvalidException,
                          scv.check_event_body, {'a': 'a', 'b': 'b'})

    def test_check_email_validation(self):
        self.assertTrue(scv.check_email_validation("anzhela.iondem@gmail.com"))
        self.assertTrue(scv.check_email_validation("angela@yahoo.com"))
        self.assertRaises(InvalidEmailException,
                          scv.check_email_validation, "angela@gmail")
        self.assertRaises(InvalidEmailException,
                          scv.check_email_validation, "angela")
