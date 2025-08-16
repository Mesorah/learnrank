import lxml.html
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..helpers import create_user

User = get_user_model()


class TestPasswordResetAuthorForm(TestCase):
    def setUp(self):
        create_user(client=self.client, auto_login=True)

        return super().setUp()

    def test_renders_input_form(self):
        response = self.client.get(reverse('authors:password_reset'))
        parsed = lxml.html.fromstring(response.content)  # HTML -> DOM
        [form] = parsed.cssselect('form[method=POST]')  # -> Search a form

        [input] = form.cssselect(f'input[name={'email'}]')
        self.assertEqual(input.get('type'), 'email')
