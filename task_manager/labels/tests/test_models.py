from task_manager.labels.models import Label
from task_manager.labels.tests import LabelTestCase


class LabelModelTest(LabelTestCase):
    def label_creation_test(self):
        data = self.test_label["create"]["valid"]

        label = Label.objects.create(**data)

        self.assertTrue(isinstance(label, Label))
        self.assertEqual(label.name, data["name"])
        self.assertEqual(label.date_created, data["date_created"])

    def label_invalid_creation_test(self):
        data = self.test_label["create"]["invalid"]

        with self.assertRaises(ValueError):
            Label.objects.create(**data)
