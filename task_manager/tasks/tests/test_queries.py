from django.urls import reverse

from task_manager.tasks.forms import TaskForm
from task_manager.tasks.tests.testcase import TaskTestCase


class TaskListViewTest(TaskTestCase):
    def setUp(self):
        self.url = reverse("task_list")
        super().setUp()

    def test_task_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_list.html")

    def test_task_list_context(self):
        response = self.client.get(self.url)
        context = response.context["tasks"]
        self.assertEqual(len(context), self.count)
        self.assertQuerySetEqual(context, self.tasks, ordered=False)

    def test_task_list_not_logged(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

    def test_filter_task_by_status(self):
        response = self.client.get(self.url, data={"status": 2})
        self.assertEqual(response.context["tasks"].count(), 1)
        self.assertContains(response, self.task3.name)

    def test_filter_task_by_author(self):
        response = self.client.get(self.url, data={"author": 2})
        self.assertEqual(response.context["tasks"].count(), 2)
        self.assertContains(response, self.task1.name)
        self.assertContains(response, self.task2.name)

    def test_filter_task_by_executor(self):
        response = self.client.get(self.url, data={"executor": 2})
        self.assertEqual(response.context["tasks"].count(), 2)
        self.assertContains(response, self.task2.name)
        self.assertContains(response, self.task3.name)

    def test_filter_task_by_labels(self):
        response = self.client.get(self.url, data={"labels": [1]})
        self.assertEqual(response.context["tasks"].count(), 2)
        self.assertContains(response, self.task2.name)
        self.assertContains(response, self.task3.name)

    def test_filter_task_by_author_and_executor(self):
        response = self.client.get(self.url, data={"author": 2, "executor": 2})
        self.assertEqual(response.context["tasks"].count(), 1)
        self.assertContains(response, self.task2.name)


class CreateTaskViewTest(TaskTestCase):
    def setUp(self):
        self.url = reverse("task_create")
        super().setUp()

    def test_create_task_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "form.html")

    def test_create_task_view_context(self):
        response = self.client.get(self.url)
        form = response.context["form"]
        self.assertTrue(isinstance(form, TaskForm))

    def test_create_task_view_not_logged(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))


class UpdateTaskViewTest(TaskTestCase):
    def setUp(self):
        self.url = reverse("task_update", kwargs={"pk": 1})
        super().setUp()

    def test_update_task_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "form.html")

    def test_update_task_view_context(self):
        response = self.client.get(self.url)
        form = response.context["form"]
        self.assertTrue(isinstance(form, TaskForm))

    def test_update_task_view_not_logged(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))


class DeleteTaskViewTest(TaskTestCase):
    def setUp(self):
        self.url = reverse("task_delete", kwargs={"pk": 1})
        super().setUp()

    def test_delete_task_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "delete.html")

    def test_delete_task_view_not_logged(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
