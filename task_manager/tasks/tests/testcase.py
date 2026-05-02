from django.test import TestCase

from task_manager.helpers import load_data


class TaskTestCase(TestCase):
    test_task = load_data("task_manager/fixtures/test_task.json")

    def setUp(self):
        ...