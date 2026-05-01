from django.urls import reverse

from task_manager.statuses.tests.testcase import StatusTestCase


class StatusListViewTest(StatusTestCase):
    def setUp(self):
        self.url = reverse("status_list")
        super().setUp()

    def test_statuses_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "status_list.html")


class CreateStatusViewTest(StatusTestCase):
    def setUp(self):
        self.url = reverse("status_create")
        super().setUp()

    def test_create_status_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "form.html")


class UpdateStatusViewTest(StatusTestCase):
    def setUp(self):
        self.url = reverse("status_update", kwargs={"pk": 1})
        super().setUp()

    def test_update_status_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "form.html")


class DeleteStatusViewTest(StatusTestCase):
    def setUp(self):
        self.url = reverse("status_delete", kwargs={"pk": 1})
        super().setUp()

    def test_delete_status_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "delete.html")
