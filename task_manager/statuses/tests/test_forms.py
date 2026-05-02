from task_manager.statuses.forms import StatusForm
from task_manager.statuses.tests.testcase import StatusTestCase


class StatusFormTest(StatusTestCase):
    def test_valid_form(self):
        status_data = self.test_status["create"]["valid"]
        form = StatusForm(data=status_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        status_data = self.test_status["create"]["invalid"]
        form = StatusForm(data=status_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
