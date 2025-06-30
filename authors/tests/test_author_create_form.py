from django.test import TestCase

from authors.forms import CustomSignupForm


class TestAuthorCreateForm(TestCase):
    def setUp(self):
        self.form_data = {
            'username': 'testing',
            'email': 'testing@example.com',
            'password1': 'testing12!@1dsFG',
            'password2': 'testing12!@1dsFG',
        }

        return super().setUp()

    def test_username_validator_is_correct(self):
        self.form_data['username'] = 'abc'

        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())

        self.form_data['username'] = 'abcd'
        form = CustomSignupForm(data=self.form_data)
        self.assertTrue(form.is_valid())

        # Username already in use
        self.form_data['username'] = 'abcd'
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_email_validator_is_correct(self):
        form = CustomSignupForm(data=self.form_data)
        self.assertTrue(form.is_valid())

        # Email already in use
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_password_validator_is_correct(self):
        self.form_data['password1'] = '1234567'
        self.form_data['password2'] = '1234567'
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())

        self.form_data['password1'] = '12345678'
        self.form_data['password2'] = '12345678'
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())

        self.form_data['password1'] = 'abcdefgh'
        self.form_data['password2'] = 'abcdefgh'
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())

        self.form_data['password1'] = 'abcdefg1'
        self.form_data['password2'] = 'abcde1fg1'
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())

        self.form_data['password1'] = 'abcdef1!'
        self.form_data['password2'] = 'abcdef1!'
        form = CustomSignupForm(data=self.form_data)
        self.assertTrue(form.is_valid())
