from django.test import TestCase
from django.urls import resolve, reverse

from authors.views import create_author


class TestAuthorCreate(TestCase):
    def test_view_is_correct(self):
        response = resolve(reverse('authors:signup'))

        self.assertEqual(response.func, create_author)

    def test_view_load_correct_template(self):
        response = self.client.get(reverse('authors:signup'))

        self.assertTemplateUsed(
            response,
            'authors/pages/authors.html'
        )

    def test_status_code_view_get_is_correct(self):
        response = self.client.get(reverse('authors:signup'))

        self.assertEqual(response.status_code, 200)

    def test_status_code_view_post_is_correct(self):
        data = {
            'username': 'testing',
            'email': 'testing@example.com',
            'password1': 'testing12!@1dsFG',
            'password2': 'testing12!@1dsFG',
        }

        response = self.client.post(reverse('authors:signup'), data)

        self.assertEqual(response.status_code, 302)
