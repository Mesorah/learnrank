import lxml.html
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()


class TestPasswordResetConfirmAuthorForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user', password='oldpassword'
        )

        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)
        self.url = reverse('authors:password_reset_confirm', kwargs={
            'uidb64': self.uidb64,
            'token': self.token
        })

        return super().setUp()

    def get_correct_url(self):
        response = self.client.get(self.url)
        redirect_url = response.url

        response = self.client.get(redirect_url)

        return redirect_url, response

    def test_new_password_validator_is_correct(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

        redirect_url = response.url

        response = self.client.get(redirect_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(redirect_url, data={
            'new_password1': 'abcd',
            'new_password2': 'defg'
        })

        self.assertContains(
            response, "The two password fields didn’t match"
        )

        response = self.client.post(redirect_url, data={
            'new_password1': 'abcd',
            'new_password2': 'abcd'
        })

        self.assertContains(
            response,
            'This password is too short. It must contain at least 8 characters'
        )

        self.assertContains(
            response, 'This password is too common.'
        )

    def test_password_user_has_been_changed(self):
        self.assertTrue(self.user.check_password('oldpassword'))

        redirect_url, _ = self.get_correct_url()

        self.client.post(redirect_url, data={
            'new_password1': 'testing12!@1dsFG',
            'new_password2': 'testing12!@1dsFG'
        })

        self.user.refresh_from_db()

        self.assertTrue(self.user.check_password('testing12!@1dsFG'))

    def test_renders_input_form(self):
        _, response = self.get_correct_url()

        parsed = lxml.html.fromstring(response.content)  # HTML -> DOM
        [form] = parsed.cssselect('form[method=POST]')  # -> Search a form

        inputs_names = {
            'new_password1': 'password',
            'new_password2': 'password'
        }
        for input_name, expected_type in inputs_names.items():
            [input] = form.cssselect(f'input[name={input_name}]')
            self.assertEqual(input.get('type'), expected_type)
