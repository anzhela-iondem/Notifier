import os
import unittest
from os.path import join, dirname, abspath

from dotenv import load_dotenv

from src.core.exceptions import FailedToGetEnvItemEntityException
from src.infrastructure.repositories import ConfigRepo


class TestConfigRepo(unittest.TestCase):

    def setUp(self) -> None:
        self.file_path = join((dirname(abspath(__file__))), ".env")
        with open(self.file_path, "w") as file:
            file.write("MAIN_APP=Flask")
        load_dotenv(self.file_path)

    def tearDown(self) -> None:
        os.remove(self.file_path)
        del os.environ["MAIN_APP"]

    def test_get_one(self):
        config_repo = ConfigRepo()
        self.assertTrue(config_repo.get_one("MAIN_APP"), {"MAIN_APP": "Flask"})
        self.assertRaises(FailedToGetEnvItemEntityException,
                          config_repo.get_one, "NN")
