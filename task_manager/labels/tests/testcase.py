from django.test import Client

from task_manager.labels.models import Label
from task_manager.tests import BaseTestCase, load_fixture_data
from task_manager.users.models import User


class LabelTestCase(BaseTestCase):
    fixtures = ["users.json", "statuses.json", "labels.json", "tasks.json"]
    test_label = load_fixture_data("test_label.json")

    def setUp(self):
        super().setUp()

        self.user = User.objects.get(pk=1)
        self.client = Client()
        self.client.force_login(self.user)

        self.label1 = Label.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=2)
        self.label3 = Label.objects.get(pk=3)
        self.labels = Label.objects.all()
        self.count = Label.objects.count()
