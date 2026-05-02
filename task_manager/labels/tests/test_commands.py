from django.contrib.messages import get_messages
from django.urls import reverse
from django.utils import translation

from task_manager.labels.models import Label
from task_manager.labels.tests.testcase import LabelTestCase


class CreateLabelTest(LabelTestCase):
    def test_create_label(self):
        data = self.test_label["create"]["valid"]
        response = self.client.post(reverse("label_create"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("label_list"))

        self.assertEqual(Label.objects.count(), self.count + 1)
        self.assertEqual(Label.objects.last().name, data["name"])

    def test_create_label_invalid(self):
        data = self.test_label["create"]["invalid"]
        response = self.client.post(reverse("label_create"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.count(), self.count)

        errors = response.context["form"].errors
        self.assertIn("name", errors)
        self.assertEqual(["This field is required."], errors["name"])

    def test_create_label_duplicate(self):
        data = self.test_label["create"]["duplicate"]
        response = self.client.post(reverse("label_create"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.count(), self.count)

        errors = response.context["form"].errors
        self.assertIn("name", errors)
        self.assertEqual(["Label with this Name already exists."], errors["name"])

    def test_create_label_too_long(self):
        data = {"name": "a" * 101}
        response = self.client.post(reverse("label_create"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.count(), self.count)

        errors = response.context["form"].errors
        self.assertIn("name", errors)
        self.assertEqual(["Ensure this value has at most 100 characters (it has 101)."], errors["name"])

    def test_create_label_not_logged_user(self):
        self.client.logout()
        data = self.test_label["create"]["valid"]
        with translation.override("ru"):
            response = self.client.post(reverse("label_create"), data=data)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("login"))

        self.assertEqual(Label.objects.count(), self.count)

        messages = get_messages(response.wsgi_request)
        self.assertIn(
            "Вы не залогинены",
            [message.message for message in messages],
        )


class UpdateLabelTest(LabelTestCase):
    def test_update_label(self):
        data = self.test_label["update"]["valid"]
        response = self.client.post(reverse("label_update", kwargs={"pk": 1}), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("label_list"))

        self.assertEqual(Label.objects.get(pk=1).name, data["name"])
        self.assertEqual(Label.objects.count(), self.count)

    def test_update_label_invalid(self):
        data = self.test_label["update"]["invalid"]
        response = self.client.post(reverse("label_update", kwargs={"pk": 1}), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.count(), self.count)

        self.assertNotEqual(Label.objects.get(pk=1).name, data["name"])
        errors = response.context["form"].errors
        self.assertIn("name", errors)
        self.assertEqual(["This field is required."], errors["name"])

    def test_update_label_not_logged_user(self):
        self.client.logout()
        data = self.test_label["update"]["valid"]
        with translation.override("ru"):
            response = self.client.post(reverse("label_update", kwargs={"pk": 1}), data=data)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("login"))

        self.assertNotEqual(Label.objects.get(pk=1).name, data["name"])

        messages = get_messages(response.wsgi_request)
        self.assertIn(
            "Вы не залогинены",
            [message.message for message in messages],
        )


class DeleteLabelTest(LabelTestCase):
    def test_delete_label(self):
        response = self.client.post(reverse("label_delete", kwargs={"pk": 3}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("label_list"))

        self.assertEqual(Label.objects.count(), self.count - 1)
        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(pk=3)

    def test_delete_label_not_logged_user(self):
        self.client.logout()
        with translation.override("ru"):
            response = self.client.post(reverse("label_delete", kwargs={"pk": 3}))
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("login"))

        self.assertEqual(Label.objects.count(), self.count)

        messages = get_messages(response.wsgi_request)
        self.assertIn(
            "Вы не залогинены",
            [message.message for message in messages],
        )

    def test_delete_bound_label(self):
        with translation.override("ru"):
            response = self.client.post(reverse("label_delete", kwargs={"pk": 2}))
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("label_list"))

        self.assertEqual(Label.objects.count(), self.count)

        messages = get_messages(response.wsgi_request)
        self.assertIn(
            "Невозможно удалить метку",
            [message.message for message in messages],
        )
