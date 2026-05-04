from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse

from task_manager.templates_enum import Template
from task_manager.users.forms import UserForm, UserUpdateForm
from task_manager.users.tests.testcase import UserTestCase


class ListUsersViewTest(UserTestCase):
    url = reverse("user_list")

    def test_list_users_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, Template.USER_LIST)

    def test_list_users_view_context(self):
        response = self.client.get(self.url)
        context_users = response.context["users"]
        self.assertEqual(len(context_users), self.count)
        self.assertQuerySetEqual(context_users, self.users, ordered=False)


class CreateUserViewTest(UserTestCase):
    url = reverse("user_create")

    def test_create_user_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, Template.FORM)

    def test_create_user_view_context(self):
        response = self.client.get(self.url)
        form = response.context["form"]
        self.assertTrue(isinstance(form, UserForm))


class LoginViewTest(UserTestCase):
    url = reverse("login")

    def test_login_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, Template.FORM)

    def test_login_view_context(self):
        response = self.client.get(self.url)
        form = response.context["form"]
        self.assertTrue(isinstance(form, AuthenticationForm))


class UpdateUserViewTest(UserTestCase):
    url = reverse("user_update", kwargs={"pk": 1})

    def test_update_user_view(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, Template.FORM)

    def test_update_user_view_context(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.url)
        form = response.context["form"]
        self.assertTrue(isinstance(form, UserUpdateForm))

    def test_update_not_logged_user_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

    def test_update_other_user_view(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user_list"))


class DeleteUserViewTest(UserTestCase):
    url = reverse("user_delete", kwargs={"pk": 1})

    def test_delete_user_view(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, Template.DELETE)

    def test_delete_not_logged_user_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

    def test_delete_other_user_view(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user_list"))
