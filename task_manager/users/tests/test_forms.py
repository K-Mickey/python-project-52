from task_manager.users.forms import UserForm, UserUpdateForm
from task_manager.users.tests.testcase import UserTestCase


class UserFormTest(UserTestCase):
    def test_valid_user_form(self):
        user_data = self.test_user["create"]["valid"]
        form = UserForm(data=user_data)
        self.assertTrue(form.is_valid())

    def test_invalid_user_form(self):
        user_data = self.test_user["create"]["invalid"]
        form = UserForm(data=user_data)
        self.assertFalse(form.is_valid())


class UserUpdateFormTest(UserTestCase):
    def test_valid_user_update_form(self):
        user_data = self.test_user["update"]["valid"]
        form = UserUpdateForm(data=user_data)
        self.assertTrue(form.is_valid())

    def test_invalid_user_update_form(self):
        user_data = self.test_user["update"]["invalid"]
        form = UserUpdateForm(data=user_data)
        self.assertFalse(form.is_valid())
