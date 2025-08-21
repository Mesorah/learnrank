from urllib.parse import urlencode

from django.test import TestCase
from django.urls import resolve, reverse
from tests.helpers import create_user

from authors.views import change_information


class TestChangeInformation(TestCase):
    def get_change_information(self):
        return self.client.get(reverse('authors:change_information'))

    def test_view_is_correct(self):
        response = resolve(reverse('authors:change_information'))

        self.assertEqual(response.func, change_information)

    def test_view_load_correct_template(self):
        response = self.get_change_information()

        self.assertTemplateUsed(response, 'authors/pages/authors.html')

    def test_anonymous_user_cannot_get_the_page(self):
        response = self.get_change_information()

        expected_url = (
            f'{reverse('authors:login')}'
            f'?{urlencode({'next': reverse('authors:change_information')})}'
        )

        self.assertRedirects(response, expected_url)

    def test_post_change_username_and_return_to_dashboard(self):
        create_user(client=self.client, auto_login=True)

        response = self.client.post(
            reverse('authors:change_information'),
            data={
                'new_username': 'new_username'
            }
        )

        self.assertRedirects(response, reverse('authors:home'))
