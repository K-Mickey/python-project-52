from django.urls import reverse

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.tests.testcase import StatusTestCase
from task_manager.templates_enum import Template


class StatusListViewTest(StatusTestCase):
    def setUp(self):
        self.url = reverse("status_list")
        super().setUp()

    def test_statuses_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, Template.STATUS_LIST)

    def test_statuses_view_context(self):
        response = self.client.get(self.url)
        context_statuses = response.context["statuses"]
        self.assertEqual(len(context_statuses), self.count)
        self.assertQuerySetEqual(context_statuses, self.statuses, ordered=False)

    def test_statuses_not_logged(self):
        self.client.logout()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))


class CreateStatusViewTest(StatusTestCase):
    def setUp(self):
        self.url = reverse("status_create")
        super().setUp()

    def test_create_status_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, Template.FORM)

    def test_create_status_view_context(self):
        response = self.client.get(self.url)
        form = response.context["form"]
        self.assertTrue(isinstance(form, StatusForm))

    def test_create_status_view_not_logged(self):
        self.client.logout()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))


class UpdateStatusViewTest(StatusTestCase):
    def setUp(self):
        self.url = reverse("status_update", kwargs={"pk": 1})
        super().setUp()

    def test_update_status_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, Template.FORM)

    def test_update_status_view_context(self):
        response = self.client.get(self.url)
        form = response.context["form"]
        self.assertTrue(isinstance(form, StatusForm))

    def test_update_status_view_not_logged(self):
        self.client.logout()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))


class DeleteStatusViewTest(StatusTestCase):
    def setUp(self):
        self.url = reverse("status_delete", kwargs={"pk": 1})
        super().setUp()

    def test_delete_status_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, Template.DELETE)

    def test_delete_status_view_not_logged(self):
        self.client.logout()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
