from django.test import Client

from task_manager.statuses.models import Status
from task_manager.tests import BaseTestCase, load_fixture_data
from task_manager.users.models import User


class StatusTestCase(BaseTestCase):
    fixtures = ["users.json", "statuses.json", "tasks.json", "labels.json"]
    test_status = load_fixture_data("test_status.json")

    def setUp(self):
        super().setUp()

        self.user = User.objects.get(pk=1)
        self.client = Client()
        self.client.force_login(self.user)

        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)
        self.status3 = Status.objects.get(pk=3)

        self.statuses = Status.objects.all()
        self.count = Status.objects.count()
