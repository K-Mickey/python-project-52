from task_manager.labels.forms import LabelForm
from task_manager.labels.tests.testcase import LabelTestCase


class LabelFormTest(LabelTestCase):
    def test_valid_form(self):
        data = self.test_label["create"]["valid"]
        form = LabelForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = self.test_label["create"]["invalid"]
        form = LabelForm(data=data)
        self.assertFalse(form.is_valid())
