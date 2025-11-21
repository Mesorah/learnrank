import lxml.html
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

import authors.constants as const
import utils.constants_informations as const_informations
from authors.forms import CustomSignupForm

User = get_user_model()


class TestCreateAuthorForm(TestCase):
    def setUp(self):
        self.form_data = {
            'username': const_informations.TEST_USERNAME,
            'email': const_informations.TEST_EMAIL,
            'password1': const_informations.TEST_PASSWORD,
            'password2': const_informations.TEST_PASSWORD,
        }

        return super().setUp()

    def test_username_min_length_validator(self):
        self.form_data['username'] = 'abc'
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['username'][0], const.USERNAME_MIN_LENGTH_ERROR
        )

    def test_username_already_taken_validator(self):
        self.form_data['username'] = 'abcd'
        form = CustomSignupForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        form.save()

        # Username already in use
        self.form_data['username'] = 'abcd'
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['username'][0], const.USERNAME_ALREADY_TAKEN_ERROR
        )

    def test_email_already_registred_validator(self):
        form = CustomSignupForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        form.save()

        # Email already in use
        self.form_data['username'] = 'testing2'
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['email'][0], const.EMAIL_ALREADY_REGISTERED_ERROR
        )

    def test_password_min_length_validator(self):
        self.form_data['password1'] = 'ab12!@'
        self.form_data['password2'] = 'ab12!@'
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            const.PASSWORD1_MIN_LENGTH_ERROR,
            form.errors['password1']
        )

    def test_password_must_contain_symbols_validator(self):
        self.form_data['password1'] = '12345678a'
        self.form_data['password2'] = '12345678a'
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            const.PASSWORD_MUST_CONTAIN_SYMBOLS_ERROR,
            form.errors['password1']
        )

    def test_password_must_contain_letters_validator(self):
        self.form_data['password1'] = '12345678!'
        self.form_data['password2'] = '12345678!'
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            const.PASSWORD_MUST_CONTAIN_LETTERS_ERROR,
            form.errors['password1']
        )

    def test_password_must_contain_numbers_validator(self):
        self.form_data['password1'] = 'abcdefgh'
        self.form_data['password2'] = 'abcdefgh'
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            const.PASSWORD_MUST_CONTAIN_NUMBERS_ERROR,
            form.errors['password1']
        )

    def test_password_do_not_match_validator(self):
        self.form_data['password1'] = 'abcdefg1'
        self.form_data['password2'] = 'abcdefg11'
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            const.PASSWORDS_DO_NOT_MATCH_ERROR,
            form.errors['password2']
        )

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

        self.form_data['username'] = const_informations.TEST_USERNAME
        self.form_data['email'] = const_informations.TEST_EMAIL
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())

        self.assertEqual(User.objects.count(), 2)

    def test_renders_input_form(self):
        response = self.client.get(reverse('authors:signup'))
        parsed = lxml.html.fromstring(response.content)  # HTML -> DOM
        [form] = parsed.cssselect('form[method=POST]')  # -> Search a form
        self.assertEqual(form.get('action'), reverse('authors:signup'))

        inputs_names = {
            'username': 'text',
            'email': 'email',
            'password1': 'password',
            'password2': 'password'
        }
        for input_name, expected_type in inputs_names.items():
            [input] = form.cssselect(f'input[name={input_name}]')
            self.assertEqual(input.get('type'), expected_type)
