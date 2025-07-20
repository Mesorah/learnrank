import lxml.html
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from authors.forms import CustomSignupForm

User = get_user_model()


class TestPasswordResetAuthorForm(TestCase):
    def setUp(self):
        self.form_data = {
            'username': 'testing',
            'email': 'testing@example.com',
            'password1': 'testing12!@1dsFG',
            'password2': 'testing12!@1dsFG',
        }

        form = CustomSignupForm(data=self.form_data)
        form.save()

        self.user = self.client.login(
            username='testing', password='testing12!@1dsFG'
        )

        return super().setUp()

    def test_renders_input_form(self):
        response = self.client.get(reverse('authors:password_reset'))
        parsed = lxml.html.fromstring(response.content)  # HTML -> DOM
        [form] = parsed.cssselect('form[method=POST]')  # -> Search a form

        [input] = form.cssselect(f'input[name={'email'}]')
        self.assertEqual(input.get('type'), 'email')
