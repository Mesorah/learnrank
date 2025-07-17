from django.test import TestCase
from django.urls import resolve, reverse

from authors.forms import CustomSignupForm
from authors.views import LoginAuthorView


class TestLoginAuthor(TestCase):
    def setUp(self):
        form_data = {
            'username': 'testing',
            'email': 'testing@example.com',
            'password1': 'testing12!@1dsFG',
            'password2': 'testing12!@1dsFG',
        }

        form = CustomSignupForm(data=form_data)
        form.save()

        self.data = {
            'username': 'testing',
            'password': 'testing12!@1dsFG',
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
        response = self.client.post(
            reverse('authors:login'), self.data
        )

        response = self.client.get(reverse('authors:signup'))

        self.assertRedirects(response, reverse('home:index'))
