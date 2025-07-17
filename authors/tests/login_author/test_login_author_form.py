import lxml.html
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.translation import activate

from authors.forms import CustomAuthenticationForm, CustomSignupForm

User = get_user_model()


class TestLoginAuthorForm(TestCase):
    def setUp(self):
        form_data = {
            'username': 'testing',
            'email': 'testing@example.com',
            'password1': 'testing12!@1dsFG',
            'password2': 'testing12!@1dsFG',
        }

        form = CustomSignupForm(data=form_data)
        form.save()

        self.form_data = {
            'username': 'testing',
            'password': 'testing12!@1dsFG',
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

    # Override_settings in this test confirms that it will change the language.
    @override_settings(LANGUAGE_CODE='pt-br')
    def test_portuguese_translate_is_load_and_is_correct(self):
        activate('pt-br')

        response = self.client.get(reverse('authors:signup'))
        content = response.content.decode()

        self.assertIn('Já tem uma conta?', content)
