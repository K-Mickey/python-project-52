from django.test import Client

from task_manager.tests import BaseTestCase, load_fixture_data
from task_manager.users.models import User


class UserTestCase(BaseTestCase):
    fixtures = ["users.json", "tasks.json", "statuses.json", "labels.json"]
    test_user = load_fixture_data("test_user.json")

    def setUp(self):
        super().setUp()

        self.client = Client()

        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user3 = User.objects.get(pk=3)

        self.users = User.objects.all()
        self.count = User.objects.count()
