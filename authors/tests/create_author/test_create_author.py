from django.test import TestCase, override_settings
from django.urls import resolve, reverse
from django.utils.translation import activate

from authors.views import CreateAuthorView


class TestCreateAuthor(TestCase):
    def setUp(self):
        self.data = {
            'username': 'testing',
            'email': 'testing@example.com',
            'password1': 'testing12!@1dsFG',
            'password2': 'testing12!@1dsFG',
        }

        return super().setUp()

    def test_view_is_correct(self):
        response = resolve(reverse('authors:signup'))

        self.assertEqual(response.func.view_class, CreateAuthorView)

    def test_view_load_correct_template(self):
        response = self.client.get(reverse('authors:signup'))

        self.assertTemplateUsed(
            response,
            'authors/pages/authors.html'
        )

    def test_get_view_returns_200(self):
        response = self.client.get(reverse('authors:signup'))

        self.assertEqual(response.status_code, 200)

    def test_signup_post_logs_user_and_redirects_to_home(self):
        response = self.client.post(
            reverse('authors:signup'), self.data, follow=True
        )

        self.assertRedirects(response, reverse('home:index'))
        self.assertTrue(response.context['user'].is_authenticated)

    def test_user_authenticated_cant_get_200_in_signup(self):
        response = self.client.post(
            reverse('authors:signup'), self.data
        )

        response = self.client.get(reverse('authors:signup'))

        self.assertRedirects(response, reverse('home:index'))

    # Override_settings in this test confirms that it will change the language.
    @override_settings(LANGUAGE_CODE='pt-br')
    def test_portuguese_translate_is_load_and_is_correct(self):
        activate('pt-br')

        response = self.client.get(reverse('authors:signup'))
        self.assertContains(response, 'Já tem uma conta?')
