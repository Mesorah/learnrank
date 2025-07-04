from django.test import TestCase
from django.urls import resolve, reverse

from authors.views import CreatViewAuthor


class TestAuthorCreate(TestCase):
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

        self.assertEqual(response.func.view_class, CreatViewAuthor)

    def test_view_load_correct_template(self):
        response = self.client.get(reverse('authors:signup'))

        self.assertTemplateUsed(
            response,
            'authors/pages/authors.html'
        )

    def test_status_code_view_get_is_correct(self):
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
