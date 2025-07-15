import lxml.html
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.translation import activate

from authors.forms import CustomSignupForm

User = get_user_model()


class TestLoginAuthorForm(TestCase):
    def setUp(self):
        self.form_data = {
            'username': 'testing',
            'password': 'testing12!@1dsFG',
        }

        return super().setUp()

    def test_username_validator_is_correct(self):
        self.form_data['username'] = 'abc'
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['username'][0], 'Please enter at least 4 characters.'
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
            form.errors['username'][0], 'Username is already taken.'
        )

    def test_password_validator_is_correct(self):
        self.form_data['password1'] = '12345678'
        self.form_data['password2'] = '12345678'
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'The password must contain symbols.', form.errors['password1']
        )
        self.assertIn(
            'Password must contain letters.', form.errors['password1']
        )

        self.form_data['password1'] = 'abcdefgh'
        self.form_data['password2'] = 'abcdefgh'
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Password must contain numbers.', form.errors['password1']
        )

        self.form_data['password1'] = 'abcdefg1'
        self.form_data['password2'] = 'abcdefg11'
        form = CustomSignupForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Passwords do not match.', form.errors['password2']
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

    # Override_settings in this test confirms that it will change the language.
    @override_settings(LANGUAGE_CODE='pt-br')
    def test_portuguese_translate_is_load_and_is_correct(self):
        activate('pt-br')

        response = self.client.get(reverse('authors:signup'))
        self.assertContains(response, 'Já tem uma conta?')
