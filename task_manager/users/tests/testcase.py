from django.test import Client, TestCase

from task_manager.helpers import load_data
from task_manager.users.models import User


class UserTestCase(TestCase):
    fixtures = ["users.json", "tasks.json", "statuses.json", "labels.json"]
    test_user = load_data("task_manager/fixtures/test_user.json")

    def setUp(self):
        self.client = Client()

        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user3 = User.objects.get(pk=3)

        self.users = User.objects.all()
        self.count = User.objects.count()
