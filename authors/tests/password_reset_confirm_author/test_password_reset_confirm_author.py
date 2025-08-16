from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.test import TestCase, override_settings
from django.urls import resolve, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import activate

from authors.views import PasswordResetConfirmAuthorView

from ..helpers import create_user

User = get_user_model()


class TestPasswordResetConfirmAuthor(TestCase):
    def setUp(self):
        self.uidb64 = 'MQ'
        self.token = 'test-token'
        self.url = reverse('authors:password_reset_confirm', kwargs={
            'uidb64': self.uidb64,
            'token': self.token
        })

        return super().setUp()

    def test_view_is_correct(self):
        response = resolve(self.url)

        self.assertEqual(
            response.func.view_class, PasswordResetConfirmAuthorView
        )

    def test_view_load_correct_template(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'authors/pages/password_reset.html'
        )

    def test_get_view_returns_200(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    # Override_settings in this test confirms that it will change the language.
    @override_settings(LANGUAGE_CODE='pt-br')
    def test_portuguese_translate_is_load_and_is_correct(self):
        activate('pt-br')

        user = create_user(client=self.client)

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        url = reverse('authors:password_reset_confirm', kwargs={
            'uidb64': uidb64,
            'token': token
        })

        response = self.client.get(url)
        redirect_url = response.url

        response = self.client.get(redirect_url)

        self.assertContains(response, 'Nova senha:')
        self.assertContains(response, 'Confirmação da nova senha:')

        response = self.client.post(redirect_url, data={
            'new_password1': 'testing12!@1dsFG',
            'new_password2': 'testing12!@1dsFG'
        }, follow=True)

        self.assertContains(response, 'Senha alterada com sucesso!')
