from django.urls import reverse

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
