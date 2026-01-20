from django.test import TestCase
from django.urls import resolve, reverse

from courses import views


class TestClasses(TestCase):
    def test_view_is_correct(self):
        response = resolve(reverse('courses:index'))

        self.assertEqual(response.func, views.index)

    def test_view_load_correct_template(self):
        response = self.client.get(reverse('courses:index'))

        self.assertTemplateUsed(
            response,
            'courses/pages/index.html'
        )

    def test_status_code_view_get_is_correct(self):
        response = self.client.get(reverse('courses:index'))

        self.assertEqual(response.status_code, 200)
