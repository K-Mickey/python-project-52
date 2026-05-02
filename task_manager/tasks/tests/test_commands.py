from django.urls import reverse

from task_manager.tasks.models import Task
from task_manager.tasks.tests.testcase import TaskTestCase


class CreateTaskTest(TaskTestCase):
    def test_create_task(self):
        data = self.test_task["create"]["valid"]
        response = self.client.post(reverse("task_create"), data=data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("task_list"))
        self.assertEqual(self.tasks.count(), self.count + 1)

        last_task = Task.objects.last()
        self.assertEqual(last_task.name, data["name"])
        self.assertEqual(last_task.description, data["description"])
        self.assertEqual(last_task.executor, self.user2)
        self.assertEqual(last_task.status, self.status)
        self.assertEqual(last_task.author, self.user2)

    def test_create_task_missing_name(self):
        data = self.test_task["create"]["invalid"]
        response = self.client.post(reverse("task_create"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.tasks.count(), self.count)

        errors = response.context["form"].errors
        self.assertIn("name", errors)

    def test_create_task_missing_description(self):
        data = self.test_task["create"]["missing_description"]
        response = self.client.post(reverse("task_create"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.tasks.count(), self.count + 1)

    def test_create_task_missing_executor(self):
        data = self.test_task["create"]["missing_executor"]
        response = self.client.post(reverse("task_create"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.tasks.count(), self.count)

        errors = response.context["form"].errors
        self.assertIn("executor", errors)

    def test_create_task_missing_status(self):
        data = self.test_task["create"]["missing_status"]
        response = self.client.post(reverse("task_create"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.tasks.count(), self.count)

        errors = response.context["form"].errors
        self.assertIn("status", errors)

    def test_create_task_duplicate(self):
        data = self.test_task["create"]["duplicate"]
        response = self.client.post(reverse("task_create"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.tasks.count(), self.count)

        errors = response.context["form"].errors
        self.assertIn("name", errors)

    def test_create_task_not_too_long(self):
        data = self.test_task["create"]["valid"].copy()
        data["name"] = "a" * 150
        data["description"] = "a" * 1000
        response = self.client.post(reverse("task_create"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.tasks.count(), self.count + 1)

    def test_create_task_too_long(self):
        data = self.test_task["create"]["valid"].copy()
        data["name"] = "a" * 151
        data["description"] = "a" * 1001
        response = self.client.post(reverse("task_create"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.tasks.count(), self.count)

        errors = response.context["form"].errors
        self.assertIn("name", errors)
        self.assertIn("description", errors)
