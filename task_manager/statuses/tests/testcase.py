from django.test import Client, TestCase

from task_manager.helpers import load_data
from task_manager.statuses.models import Status
from task_manager.users.models import User


class StatusTestCase(TestCase):
    fixtures = ["users.json", "statuses.json"]
    test_status = load_data("task_manager/fixtures/test_status.json")

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client = Client()
        self.client.force_login(self.user)

        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)
        self.status3 = Status.objects.get(pk=3)

        self.statuses = Status.objects.all()
        self.count = Status.objects.count()
