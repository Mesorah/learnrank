import lxml.html
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

import utils.constants_informations as const_informations
from authors.tests.helpers import create_user

User = get_user_model()


class TestPasswordResetConfirmAuthorForm(TestCase):
    def get_correct_url(self):
        response = self.client.get(self.url)
        redirect_url = response.url

        response = self.client.get(redirect_url)

        return redirect_url, response

    def setUp(self):
        self.user = create_user(client=self.client, password='oldpassword')

        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)
        self.url = reverse('authors:password_reset_confirm', kwargs={
            'uidb64': self.uidb64,
            'token': self.token
        })

        self.redirect_url, self.response = self.get_correct_url()

        return super().setUp()

    def test_new_password_do_not_match_validator(self):
        response = self.client.post(self.redirect_url, data={
            'new_password1': 'abcdefg1',
            'new_password2': 'abcdefg11'
        })

        self.assertContains(
            response, "The two password fields didn’t match"  # TODO
        )

    def test_new_password_min_length_validator(self):
        response = self.client.post(self.redirect_url, data={
            'new_password1': 'ab12!@',
            'new_password2': 'ab12!@'
        })

        self.assertContains(
            response,
            'This password is too short. It must contain at least 8 characters'
        )

    def test_new_password_common_validator(self):
        response = self.client.post(self.redirect_url, data={
            'new_password1': 'abcd',
            'new_password2': 'abcd'
        })

        self.assertContains(
            response, 'This password is too common.'
        )

    def test_password_user_has_been_changed(self):
        password = const_informations.TEST_PASSWORD

        self.assertTrue(self.user.check_password('oldpassword'))

        self.client.post(self.redirect_url, data={
            'new_password1': password,
            'new_password2': password
        })

        self.user.refresh_from_db()

        self.assertTrue(self.user.check_password(password))

    def test_renders_input_form(self):
        parsed = lxml.html.fromstring(self.response.content)  # HTML -> DOM
        [form] = parsed.cssselect('form[method=POST]')  # -> Search a form

        inputs_names = {
            'new_password1': 'password',
            'new_password2': 'password'
        }
        for input_name, expected_type in inputs_names.items():
            [input] = form.cssselect(f'input[name={input_name}]')
            self.assertEqual(input.get('type'), expected_type)
