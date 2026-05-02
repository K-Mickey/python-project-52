from django.urls import reverse

from task_manager.tasks.tests.testcase import TaskTestCase


class TaskListViewTest(TaskTestCase):
    def test_task_list_view(self):
        response = self.client.get(reverse("task_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_list.html")
