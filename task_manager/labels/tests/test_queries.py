from django.urls import reverse

from task_manager.labels.forms import LabelForm
from task_manager.labels.tests.testcase import LabelTestCase


class LabelListViewTest(LabelTestCase):
    def setUp(self):
        self.url = reverse("label_list")
        super().setUp()

    def test_labels_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "label_list.html")

    def test_labels_view_context(self):
        response = self.client.get(self.url)
        context = response.context["labels"]
        self.assertEqual(len(context), self.count)
        self.assertQuerySetEqual(context, self.labels, ordered=False)

    def test_labels_view_not_logger(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))


class CreateLabelViewTest(LabelTestCase):
    def setUp(self):
        self.url = reverse("label_create")
        super().setUp()

    def test_create_label_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "form.html")

    def test_create_label_view_context(self):
        response = self.client.get(self.url)
        form = response.context["form"]
        self.assertTrue(isinstance(form, LabelForm))

    def test_create_label_view_not_logged(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))


class UpdateLabelViewTest(LabelTestCase):
    def setUp(self):
        self.url = reverse("label_update", kwargs={"pk": 1})
        super().setUp()

    def test_update_label_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "form.html")

    def test_update_label_view_context(self):
        response = self.client.get(self.url)
        form = response.context["form"]
        self.assertTrue(isinstance(form, LabelForm))

    def test_update_label_view_not_logged(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
