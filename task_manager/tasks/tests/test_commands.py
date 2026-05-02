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


class UpdateTaskTest(TaskTestCase):
    def test_update_task(self):
        data = self.test_task["update"]["valid"]
        response = self.client.post(reverse("task_update", kwargs={"pk": 1}), data=data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("task_list"))
        self.assertEqual(self.tasks.count(), self.count)
        self.assertEqual(Task.objects.get(pk=1).name, data["name"])

    def test_update_task_invalid(self):
        data = self.test_task["update"]["invalid"]
        response = self.client.post(reverse("task_update", kwargs={"pk": 1}), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(Task.objects.get(pk=1).name, data["name"])

        errors = response.context["form"].errors
        self.assertIn("name", errors)

    def test_update_not_logged_user(self):
        self.client.logout()

        data = self.test_task["update"]["valid"]
        response = self.client.post(reverse("task_update", kwargs={"pk": 1}), data=data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
        self.assertNotEqual(Task.objects.get(pk=1).name, data["name"])


class DeleteTaskTest(TaskTestCase):
    def test_delete_task(self):
        response = self.client.post(reverse("task_delete", kwargs={"pk": 1}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("task_list"))
        self.assertEqual(self.tasks.count(), self.count - 1)

        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=1)

    def test_delete_not_logged_user(self):
        self.client.logout()

        response = self.client.post(reverse("task_delete", kwargs={"pk": 1}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
        self.assertEqual(self.tasks.count(), self.count)

    def test_delete_not_owner(self):
        response = self.client.post(reverse("task_delete", kwargs={"pk": 3}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("task_list"))
        self.assertEqual(self.tasks.count(), self.count)
