from django.test import TestCase
from django.urls import resolve, reverse

from home import views


class TestHomeIndex(TestCase):
    def test_view_is_correct(self):
        response = resolve(reverse('home:index'))

        self.assertEqual(response.func, views.index)

    def test_view_load_correct_template(self):
        response = self.client.get(reverse('home:index'))

        self.assertTemplateUsed(
            response,
            'home/pages/index.html'
        )

    def test_status_code_view_get_is_correct(self):
        response = self.client.get(reverse('home:index'))

        self.assertEqual(response.status_code, 200)


class TestClasses(TestCase):
    def test_view_is_correct(self):
        response = resolve(reverse('home:classes'))

        self.assertEqual(response.func, views.classes)

    def test_view_load_correct_template(self):
        response = self.client.get(reverse('home:classes'))

        self.assertTemplateUsed(
            response,
            'home/pages/classes.html'
        )

    def test_status_code_view_get_is_correct(self):
        response = self.client.get(reverse('home:classes'))

        self.assertEqual(response.status_code, 200)
