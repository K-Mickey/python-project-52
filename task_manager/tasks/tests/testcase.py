from django.test import Client

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.tests import BaseTestCase, load_fixture_data
from task_manager.users.models import User


class TaskTestCase(BaseTestCase):
    fixtures = ["users.json", "statuses.json", "labels.json", "tasks.json"]
    test_task = load_fixture_data("test_task.json")

    def setUp(self):
        super().setUp()

        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)
        self.task3 = Task.objects.get(pk=3)
        self.tasks = Task.objects.all()
        self.count = Task.objects.count()

        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)

        self.status = Status.objects.get(pk=1)
        self.label = Label.objects.get(pk=1)

        self.client = Client()
        self.client.force_login(self.user2)
