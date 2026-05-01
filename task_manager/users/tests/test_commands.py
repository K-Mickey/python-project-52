from django.contrib.auth import get_user
from django.urls import reverse

from task_manager.users.models import User
from task_manager.users.tests.testcase import UserTestCase


class LoginTest(UserTestCase):
    def setUp(self):
        self.url = reverse("login")
        super().setUp()

    def test_login_success(self):
        self.user1.set_password("secret382")
        self.user1.save()

        response = self.client.post(
            self.url,
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


class LogoutTest(UserTestCase):
    def setUp(self):
        self.url = reverse("logout")
        super().setUp()

    def test_logout_success(self):
        self.client.force_login(self.user1)
        self.assertTrue(get_user(self.client).is_authenticated)

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

        self.assertFalse(get_user(self.client).is_authenticated)


class CreateUserTest(UserTestCase):
    def setUp(self):
        self.url = reverse("user_create")
        super().setUp()

    def test_create_user_success(self):
        user_data = self.test_user["create"]["valid"]
        response = self.client.post(self.url, data=user_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        self.assertEqual(User.objects.count(), self.count + 1)
        self.assertEqual(User.objects.last().username, user_data["username"])

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
    def setUp(self):
        self.url = reverse("user_update", kwargs={"pk": 1})
        super().setUp()

    def test_update_user_success(self):
        self.client.force_login(self.user1)

        user_data = self.test_user["update"]["valid"]
        response = self.client.post(self.url, data=user_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user_list"))

        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, user_data["first_name"])
        self.assertEqual(self.user1.last_name, user_data["last_name"])

        self.assertEqual(User.objects.count(), self.count)

    def test_update_user_fail(self):
        self.client.force_login(self.user1)

        user_data = self.test_user["update"]["invalid"]
        response = self.client.post(self.url, data=user_data)

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
        response = self.client.post(self.url, data=user_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user_list"))

        self.user1.refresh_from_db()
        self.assertNotEqual(self.user1.first_name, user_data["first_name"])
        self.assertNotEqual(self.user1.last_name, user_data["last_name"])
        self.assertEqual(User.objects.count(), self.count)


class DeleteUserTest(UserTestCase):
    def setUp(self):
        self.url = reverse("user_delete", kwargs={"pk": 1})
        super().setUp()

    def test_delete_user_success(self):
        self.client.force_login(self.user1)

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user_list"))

        self.assertEqual(User.objects.count(), self.count - 1)

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=1)

    def test_delete_other_user(self):
        self.client.force_login(self.user2)

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user_list"))

        self.assertEqual(User.objects.count(), self.count)

    def test_delete_not_logged_user(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        self.assertEqual(User.objects.count(), self.count)
