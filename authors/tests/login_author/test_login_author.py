from django.test import TestCase, override_settings
from django.urls import resolve, reverse
from django.utils.translation import activate

import utils.constants_informations as const_informations
from authors.views import LoginAuthorView

from ..helpers import create_user


class TestLoginAuthor(TestCase):
    def setUp(self):
        create_user(client=self.client)

        self.data = {
            'username': const_informations.TEST_USERNAME,
            'password': const_informations.TEST_PASSWORD,
        }

        return super().setUp()

    def test_view_is_correct(self):
        response = resolve(reverse('authors:login'))

        self.assertEqual(response.func.view_class, LoginAuthorView)

    def test_view_load_correct_template(self):
        response = self.client.get(reverse('authors:login'))

        self.assertTemplateUsed(
            response,
            'authors/pages/authors.html'
        )

    def test_get_view_returns_200(self):
        response = self.client.get(reverse('authors:login'))

        self.assertEqual(response.status_code, 200)

    def test_signup_post_logs_user_and_redirects_to_home(self):
        response = self.client.post(
            reverse('authors:login'), self.data, follow=True
        )

        self.assertRedirects(response, reverse('home:index'))
        self.assertTrue(response.context['user'].is_authenticated)

    def test_user_authenticated_cant_get_200_in_signup(self):
        self.client.post(
            reverse('authors:login'), self.data
        )

        response = self.client.get(reverse('authors:login'))

        self.assertRedirects(response, reverse('home:index'))

    # Override_settings in this test confirms that it will change the language.
    @override_settings(LANGUAGE_CODE='pt-br')
    def test_portuguese_translate_is_load_and_is_correct(self):
        activate('pt-br')

        response = self.client.get(reverse('authors:login'))
        content = response.content.decode()

        self.assertIn('Ainda não tem uma conta?', content)
        self.assertIn('Esqueceu sua senha?', content)
