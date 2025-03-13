from django.test import TestCase
from home.forms import UserRegisterForm
from django.contrib.auth.models import User


class TestRegistrationForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='milad', email='milad@yahoo.com', password='milad')

    def test_valid_form(self):
        form = UserRegisterForm(
            data={'username': 'kevin', 'email': 'kevin@yahoo.com', 'first_name': 'kevin', 'last_name': 'kelvin',
                  'password': 'kevin',
                  'confirm_password': 'kevin'})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = UserRegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)

    def test_valid_form_email(self):
        form = UserRegisterForm(
            data={'username': 'kevin', 'email': 'milad@yahoo.com', 'first_name': 'kevin', 'last_name': 'kelvin',
                  'password': 'kevin',
                  'confirm_password': 'kevin'})
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('email'))

    def test_valid_form_username(self):
        form = UserRegisterForm(
            data={'username': 'milad', 'email': 'kevin@yahoo.com', 'first_name': 'kevin', 'last_name': 'kelvin',
                  'password': 'kevin',
                  'confirm_password': 'kevin'})
        self.assertEqual(len(form.errors), 1)

    def test_valid_form_confirm_password(self):
        form = UserRegisterForm(data={'username': 'kevin', 'email': 'kevin@yahoo.com', 'first_name': 'kevin', 'last_name': 'kelvin',
                  'password': 'kevin',
                  'confirm_password': 'jim'})
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error)


# TODO:create login test