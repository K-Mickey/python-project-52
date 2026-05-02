from django.contrib.auth import get_user
from django.contrib.messages import get_messages
from django.urls import reverse
from django.utils import translation

from task_manager.users.models import User
from task_manager.users.tests.testcase import UserTestCase


class LoginTest(UserTestCase):
    def test_login_success(self):
        self.user1.set_password("secret382")
        self.user1.save()

        with translation.override("ru"):
            url = reverse("login")
            response = self.client.post(
                url,
                data={
                    "username": self.user1.username,
                    "password": "secret382",
                },
            )

            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("index"))

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.username, self.user1.username)

        messages = get_messages(response.wsgi_request)
        self.assertIn(
            "Вы залогинены",
            [message.message for message in messages],
        )


class LogoutTest(UserTestCase):
    def test_logout_success(self):
        self.client.force_login(self.user1)
        self.assertTrue(get_user(self.client).is_authenticated)

        with translation.override("ru"):
            url = reverse("logout")
            response = self.client.post(url)

            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("index"))

        self.assertFalse(get_user(self.client).is_authenticated)

        messages = get_messages(response.wsgi_request)
        self.assertIn(
            "Вы разлогинены",
            [message.message for message in messages],
        )


class CreateUserTest(UserTestCase):
    def setUp(self):
        self.url = reverse("user_create")
        super().setUp()

    def test_create_user_success(self):
        user_data = self.test_user["create"]["valid"]
        with translation.override("ru"):
            url = reverse("user_create")
            response = self.client.post(url, data=user_data)

            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("login"))

        self.assertEqual(User.objects.count(), self.count + 1)
        self.assertEqual(User.objects.last().username, user_data["username"])

        messages = get_messages(response.wsgi_request)
        self.assertIn(
            "Пользователь успешно зарегистрирован",
            [message.message for message in messages],
        )

    def test_create_invalid_username(self):
        user_data = self.test_user["create"]["invalid"]
        response = self.client.post(self.url, data=user_data)

        errors = response.context["form"].errors
        self.assertIn("username", errors)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_duplicate_user(self):
        user_data = self.test_user["create"]["duplicate"]
        response = self.client.post(self.url, data=user_data)

        errors = response.context["form"].errors
        self.assertIn("username", errors)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_missing_fields(self):
        user_data = self.test_user["create"]["missing_fields"]
        response = self.client.post(self.url, data=user_data)

        errors = response.context["form"].errors
        self.assertIn("username", errors)
        self.assertIn("first_name", errors)
        self.assertIn("last_name", errors)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_password_mismatch(self):
        user_data = self.test_user["create"]["password_mismatch"]
        response = self.client.post(self.url, data=user_data)

        errors = response.context["form"].errors
        self.assertIn("password2", errors)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_password_too_short(self):
        user_data = self.test_user["create"]["password_too_short"]
        response = self.client.post(self.url, data=user_data)

        errors = response.context["form"].errors
        self.assertIn("password2", errors)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_password_missing(self):
        user_data = self.test_user["create"]["password_missing"]
        response = self.client.post(self.url, data=user_data)

        errors = response.context["form"].errors
        self.assertIn("password1", errors)
        self.assertIn("password2", errors)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)


class UpdateUserTest(UserTestCase):
    def test_update_user_success(self):
        self.client.force_login(self.user1)

        user_data = self.test_user["update"]["valid"]

        with translation.override("ru"):
            url = reverse("user_update", kwargs={"pk": 1})
            response = self.client.post(url, data=user_data)

            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("user_list"))

        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, user_data["first_name"])
        self.assertEqual(self.user1.last_name, user_data["last_name"])

        self.assertEqual(User.objects.count(), self.count)

        messages = get_messages(response.wsgi_request)
        self.assertIn(
            "Пользователь успешно изменен",
            [message.message for message in messages],
        )

    def test_update_user_fail(self):
        self.client.force_login(self.user1)

        user_data = self.test_user["update"]["invalid"]
        url = reverse("user_update", kwargs={"pk": 1})
        response = self.client.post(url, data=user_data)

        errors = response.context["form"].errors
        self.assertIn("username", errors)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

        self.user1.refresh_from_db()
        self.assertNotEqual(self.user1.first_name, user_data["first_name"])
        self.assertNotEqual(self.user1.last_name, user_data["last_name"])

    def test_update_other_user(self):
        self.client.force_login(self.user2)

        user_data = self.test_user["update"]["valid"]
        with translation.override("ru"):
            url = reverse("user_update", kwargs={"pk": 1})
            response = self.client.post(url, data=user_data)

            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("user_list"))

        self.user1.refresh_from_db()
        self.assertNotEqual(self.user1.first_name, user_data["first_name"])
        self.assertNotEqual(self.user1.last_name, user_data["last_name"])
        self.assertEqual(User.objects.count(), self.count)

        messages = get_messages(response.wsgi_request)
        self.assertIn(
            "У вас нет прав для изменения",
            [message.message for message in messages],
        )

    def test_update_not_logged_user(self):
        with translation.override("ru"):
            url = reverse("user_update", kwargs={"pk": 1})
            response = self.client.post(url)

            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("login"))

        self.assertEqual(User.objects.count(), self.count)

        messages = get_messages(response.wsgi_request)
        self.assertIn(
            "Вы не залогинены",
            [message.message for message in messages],
        )


class DeleteUserTest(UserTestCase):
    def test_delete_user_success(self):
        self.client.force_login(self.user1)

        with translation.override("ru"):
            url = reverse("user_delete", kwargs={"pk": 1})
            response = self.client.post(url)

            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("user_list"))

        self.assertEqual(User.objects.count(), self.count - 1)

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=1)

        messages = get_messages(response.wsgi_request)
        self.assertIn(
            "Пользователь успешно удален",
            [message.message for message in messages],
        )

    def test_delete_other_user(self):
        self.client.force_login(self.user2)

        with translation.override("ru"):
            url = reverse("user_delete", kwargs={"pk": 1})
            response = self.client.post(url)

            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("user_list"))

        self.assertEqual(User.objects.count(), self.count)

        messages = get_messages(response.wsgi_request)
        self.assertIn(
            "У вас нет прав для изменения",
            [message.message for message in messages],
        )

    def test_delete_not_logged_user(self):
        with translation.override("ru"):
            url = reverse("user_delete", kwargs={"pk": 1})
            response = self.client.post(url)

            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("login"))

        self.assertEqual(User.objects.count(), self.count)

        messages = get_messages(response.wsgi_request)
        self.assertIn(
            "Вы не залогинены",
            [message.message for message in messages],
        )

    def test_delete_bound_user(self):
        self.client.force_login(self.user3)

        with translation.override("ru"):
            url = reverse("user_delete", kwargs={"pk": 3})
            response = self.client.post(url)

            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("user_list"))

        self.assertEqual(User.objects.count(), self.count)

        messages = get_messages(response.wsgi_request)
        self.assertIn(
            "Невозможно удалить пользователя",
            [message.message for message in messages],
        )
