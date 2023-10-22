import json
import unittest
from os.path import join, dirname, abspath

from flask import Flask

from src.infrastructure.controllers import APIController
from tests.events.expected_responses import ExpectedResults


class TestAPIController(unittest.TestCase):

    def setUp(self) -> None:
        self.app = Flask(__name__)
        self.api_controller = APIController()
        self.expected_result = ExpectedResults()

    def tearDown(self) -> None:
        del self.app
        del self.api_controller
        del self.expected_result

    def test_controller_new_publication(self) -> None:
        expected_result = self.expected_result.get_result_new_publication
        actual_list = []
        file_path_new_publication = join(dirname(dirname(abspath(__file__))),
                                         "events", "new_publication.json")
        with open(file_path_new_publication) as file:
            json_file_data = json.load(file)
            for i in json_file_data:
                with self.app.app_context():
                    response_object, code = self.api_controller.process_event(i)
                    actual_list.append((response_object.json, code))
            self.assertTrue(actual_list == expected_result)

    def test_controller_approved_publication(self) -> None:
        expected_result = self.expected_result.get_result_approved_publication
        actual_list = []
        file_path_new_publication = join(dirname(dirname(abspath(__file__))),
                                         "events", "approved_publication.json")
        with open(file_path_new_publication) as file:
            json_file_data = json.load(file)
            for i in json_file_data:
                with self.app.app_context():
                    response_object, code = self.api_controller.process_event(i)
                    actual_list.append((response_object.json, code))
            self.assertTrue(actual_list == expected_result)
