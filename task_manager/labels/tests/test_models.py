from django.utils import timezone

from task_manager.labels.models import Label
from task_manager.labels.tests.testcase import LabelTestCase


class LabelModelTest(LabelTestCase):
    def test_label_valid_creation(self):
        data = self.test_label["create"]["valid"]
        label = Label.objects.create(
            name=data["name"],
            date_created=timezone.now(),
        )

        self.assertTrue(isinstance(label, Label))
        self.assertEqual(label.name, data["name"])
