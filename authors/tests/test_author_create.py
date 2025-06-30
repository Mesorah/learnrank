from django.test import TestCase
from django.urls import resolve, reverse

from authors.views import create_author


class TestAuthorCreate(TestCase):
    def test_view_is_correct(self):
        response = resolve(reverse('signup'))

        self.assertEqual(response.func, create_author)

    def test_view_load_correct_template(self):
        response = self.client.get(reverse('signup'))

        self.assertTemplateUsed(
            response,
            'authors/pages/authors.html'
        )

    def test_status_code_view_get_is_correct(self):
        response = self.client.get(reverse('signup'))

        self.assertEqual(response.status_code, 200)
