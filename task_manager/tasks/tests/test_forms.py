from task_manager.tasks.forms import TaskForm
from task_manager.tasks.tests.testcase import TaskTestCase


class TaskFormTest(TaskTestCase):
    def test_valid_form(self):
        data = self.test_task['create']['valid']
        form = TaskForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = self.test_task['create']['invalid']
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())