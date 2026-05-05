from django.contrib.messages import get_messages
from django.urls import reverse
from django.utils import translation

from task_manager.statuses.models import Status
from task_manager.statuses.tests.testcase import StatusTestCase


class CreateStatusTest(StatusTestCase):
    def test_create_status_success(self):
        data = self.test_status["create"]["valid"]
        with translation.override("ru"):
            response = self.client.post(reverse("status_create"), data=data)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("status_list"))

        self.assertEqual(self.statuses.count(), self.count + 1)
        self.assertEqual(self.statuses.last().name, data["name"])

        messages = get_messages(response.wsgi_request)
        self.assertIn(
            "Статус успешно создан",
            [message.message for message in messages],
        )

    def test_create_status_invalid(self):
        data = self.test_status["create"]["invalid"]
        response = self.client.post(reverse("status_create"), data=data)

        errors = response.context["form"].errors
        self.assertIn("name", errors)
        self.assertEqual(["This field is required."], errors["name"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.statuses.count(), self.count)

    def test_create_status_duplicate(self):
        data = self.test_status["create"]["duplicate"]
        response = self.client.post(reverse("status_create"), data=data)

        errors = response.context["form"].errors
        self.assertIn("name", errors)
        self.assertEqual(
            ["Status with this Name already exists."], errors["name"]
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.statuses.count(), self.count)

    def test_create_status_too_long(self):
        data = {"name": "a" * 101}
        response = self.client.post(reverse("status_create"), data=data)

        errors = response.context["form"].errors
        self.assertIn("name", errors)
        self.assertEqual(
            ["Ensure this value has at most 100 characters (it has 101)."],
            errors["name"],
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.statuses.count(), self.count)

    def test_create_status_not_logged_user(self):
        self.client.logout()

        data = self.test_status["create"]["valid"]
        with translation.override("ru"):
            response = self.client.post(reverse("status_create"), data=data)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("login"))

        self.assertEqual(self.statuses.count(), self.count)

        messages = get_messages(response.wsgi_request)
        self.assertIn(
            "Вы не залогинены",
            [message.message for message in messages],
        )


class UpdateStatusTest(StatusTestCase):
    def test_update_status_success(self):
        data = self.test_status["update"]["valid"]
        with translation.override("ru"):
            response = self.client.post(
                reverse("status_update", kwargs={"pk": 1}), data=data
            )
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("status_list"))

        self.assertEqual(self.statuses.count(), self.count)
        self.assertEqual(Status.objects.get(pk=1).name, data["name"])

        messages = get_messages(response.wsgi_request)
        self.assertIn(
            "Статус успешно изменен",
            [message.message for message in messages],
        )

    def test_update_status_invalid(self):
        data = self.test_status["update"]["invalid"]
        response = self.client.post(
            reverse("status_update", kwargs={"pk": 1}), data=data
        )

        errors = response.context["form"].errors
        self.assertIn("name", errors)
        self.assertEqual(["This field is required."], errors["name"])

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(Status.objects.get(pk=1).name, data["name"])

    def test_update_status_not_logged_user(self):
        self.client.logout()

        data = self.test_status["update"]["valid"]
        with translation.override("ru"):
            response = self.client.post(
                reverse("status_update", kwargs={"pk": 1}), data=data
            )
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("login"))

        self.assertNotEqual(Status.objects.get(pk=1).name, data["name"])

        messages = get_messages(response.wsgi_request)
        self.assertIn(
            "Вы не залогинены",
            [message.message for message in messages],
        )


class DeleteStatusTest(StatusTestCase):
    def test_delete_status_success(self):
        with translation.override("ru"):
            response = self.client.post(
                reverse("status_delete", kwargs={"pk": 1})
            )
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("status_list"))

        self.assertEqual(self.statuses.count(), self.count - 1)
        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(pk=1)

        messages = get_messages(response.wsgi_request)
        self.assertIn(
            "Статус успешно удален",
            [message.message for message in messages],
        )

    def test_delete_status_not_logged_user(self):
        self.client.logout()

        with translation.override("ru"):
            response = self.client.post(
                reverse("status_delete", kwargs={"pk": 1})
            )
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("login"))

        self.assertEqual(self.statuses.count(), self.count)

        messages = get_messages(response.wsgi_request)
        self.assertIn(
            "Вы не залогинены",
            [message.message for message in messages],
        )

    def test_delete_bound_status(self):
        with translation.override("ru"):
            response = self.client.post(
                reverse("status_delete", kwargs={"pk": 2})
            )
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("status_list"))

        self.assertEqual(self.statuses.count(), self.count)

        messages = get_messages(response.wsgi_request)
        self.assertIn(
            "Невозможно удалить статус",
            [message.message for message in messages],
        )
