from django.test import TestCase, override_settings
from django.urls import resolve, reverse
from django.utils.translation import activate

from authors.views import PasswordResetDoneAuthorView


class TestPasswordResetAuthor(TestCase):
    def test_view_is_correct(self):
        response = resolve(reverse('authors:password_reset_done'))

        self.assertEqual(response.func.view_class, PasswordResetDoneAuthorView)

    def test_view_load_correct_template(self):
        response = self.client.get(reverse('authors:password_reset_done'))

        self.assertTemplateUsed(
            response,
            'authors/pages/password_reset_done.html'
        )

    def test_get_view_returns_200(self):
        response = self.client.get(reverse('authors:password_reset_done'))

        self.assertEqual(response.status_code, 200)

    # Override_settings in this test confirms that it will change the language.
    @override_settings(LANGUAGE_CODE='pt-br')
    def test_portuguese_translate_is_load_and_is_correct(self):
        activate('pt-br')

        response = self.client.get(reverse('authors:password_reset_done'))
        self.assertContains(response, 'Verifique seu e-mail')

        content = response.content.decode()
        self.assertIn(
            'Se existir uma conta associada ao endereço de e-mail '
            'fornecido, você receberá uma mensagem com instruções para '
            'redefinir sua senha.', content
        )
