import json

from django.conf import settings
from django.test import TestCase


class BaseTestCase(TestCase):
    def setUp(self):
        settings.ROLLBAR = {"enabled": False}


def load_fixture_data(fixture_name):
    file_path = settings.BASE_DIR / "task_manager" / "fixtures" / f"{fixture_name}"
    file_data = file_path.read_text()
    return json.loads(file_data)
