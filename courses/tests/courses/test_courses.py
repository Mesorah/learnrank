from urllib.parse import urlencode

from django.test import TestCase
from django.urls import resolve, reverse

from authors.tests.helpers import create_user
from courses import views


class TestClasses(TestCase):
    def test_view_is_correct(self):
        response = resolve(reverse('courses:index'))

        self.assertEqual(response.func, views.index)

    def test_view_load_correct_template(self):
        create_user(auto_login=True, client=self.client)
        response = self.client.get(reverse('courses:index'))

        self.assertTemplateUsed(
            response,
            'courses/pages/index.html'
        )

    def test_status_code_view_get_is_correct(self):
        create_user(auto_login=True, client=self.client)
        response = self.client.get(reverse('courses:index'))

        self.assertEqual(response.status_code, 200)

    def test_user_not_logged_in_cannot_enter_to_the_courses_page(self):
        response = self.client.get(reverse('courses:index'))

        expected_url = (
            f"{reverse('authors:login')}"
            f"?{urlencode({'next': reverse('courses:index')})}"
        )

        self.assertRedirects(response, expected_url)
