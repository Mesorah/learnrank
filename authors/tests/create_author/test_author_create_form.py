from django.contrib.auth import get_user_model
from django.test import TestCase

from authors.forms import CustomSignupForm

User = get_user_model()


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
        self.assertEqual(
            form.errors['username'][0], 'Size less than 4 characters.'
        )

        self.form_data['username'] = 'abcd'
        form = CustomSignupForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        form.save()

        # Username already in use
        self.form_data['username'] = 'abcd'
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['username'][0], 'Username already in use.'
        )

    def test_email_validator_is_correct(self):
        form = CustomSignupForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        form.save()

        # Email already in use
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['email'][0], 'Email already in use.'
        )

    def test_password_validator_is_correct(self):
        self.form_data['password1'] = '12345678'
        self.form_data['password2'] = '12345678'
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Without the use of symbols.', form.errors['password1']
        )
        self.assertIn(
            'Without the use of characters.', form.errors['password1']
        )

        self.form_data['password1'] = 'abcdefgh'
        self.form_data['password2'] = 'abcdefgh'
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Without the use of numbers.', form.errors['password1']
        )

        self.form_data['password1'] = 'abcdefg1'
        self.form_data['password2'] = 'abcdefg11'
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Passwords are not the same.', form.errors['password2']
        )

        self.form_data['password1'] = 'abcdef1!'
        self.form_data['password2'] = 'abcdef1!'
        form = CustomSignupForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_user_is_created(self):
        form = CustomSignupForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        form.save()

        self.assertEqual(User.objects.count(), 1)

        self.form_data['username'] = 'testing2'
        self.form_data['email'] = 'testing2@example.com'
        form = CustomSignupForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        form.save()

        self.assertEqual(User.objects.count(), 2)

        self.form_data['username'] = 'testing'
        self.form_data['email'] = 'testing@example.com'
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())

        self.assertEqual(User.objects.count(), 2)
