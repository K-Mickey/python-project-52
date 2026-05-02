from django.test import TestCase

from task_manager.helpers import load_data


class LabelTestCase(TestCase):
    test_label = load_data("task_manager/fixtures/test_label.json")

    def setUp(self): ...
