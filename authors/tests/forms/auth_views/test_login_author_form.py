import lxml.html
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

import utils.constants_informations as const_informations
from authors.forms import CustomAuthenticationForm
from authors.tests.helpers import create_user

User = get_user_model()


class TestLoginAuthorForm(TestCase):
    def setUp(self):
        create_user(client=self.client)

        self.form_data = {
            'username': const_informations.TEST_USERNAME,
            'password': const_informations.TEST_PASSWORD,
        }

        return super().setUp()

    def test_username_validator_is_correct(self):
        self.form_data['username'] = 'abc'
        form = CustomAuthenticationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            ('Please enter a correct username and password. '
             'Note that both fields may be case-sensitive.'),
            form.errors['__all__'][0]
        )

    def test_password_validator_is_correct(self):
        self.form_data['password'] = 'abc'
        form = CustomAuthenticationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            ('Please enter a correct username and password. '
             'Note that both fields may be case-sensitive.'),
            form.errors['__all__'][0]
        )

    def test_user_is_created(self):
        form = CustomAuthenticationForm(data=self.form_data)
        self.assertTrue(form.is_valid())

        user = form.get_user()

        self.assertTrue(user.is_authenticated)

    def test_renders_input_form(self):
        response = self.client.get(reverse('authors:login'))
        parsed = lxml.html.fromstring(response.content)  # HTML -> DOM
        [form] = parsed.cssselect('form[method=POST]')  # -> Search a form
        self.assertEqual(form.get('action'), reverse('authors:login'))

        inputs_names = {
            'username': 'text',
            'password': 'password'
        }
        for input_name, expected_type in inputs_names.items():
            [input] = form.cssselect(f'input[name={input_name}]')
            self.assertEqual(input.get('type'), expected_type)
