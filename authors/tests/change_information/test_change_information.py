from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import resolve, reverse
from django.utils import timezone
from django.utils.translation import activate

import authors.constants as const
from authors.tests.helpers import create_user
from authors.views import change_information

User = get_user_model()


class TestChangeInformation(TestCase):
    def setUp(self):
        self.user = create_user(client=self.client, auto_login=True)

        return super().setUp()

    def get_change_information(self):
        return self.client.get(reverse('authors:change_information'))

    def test_view_is_correct(self):
        self.client.logout()
        response = resolve(reverse('authors:change_information'))

        self.assertEqual(response.func, change_information)

    def test_view_load_correct_template(self):
        response = self.get_change_information()

        self.assertTemplateUsed(response, 'authors/pages/authors.html')

    def test_anonymous_user_cannot_get_the_page(self):
        self.client.logout()
        response = self.get_change_information()

        expected_url = (
            f'{reverse('authors:login')}'
            f'?{urlencode({'next': reverse('authors:change_information')})}'
        )

        self.assertRedirects(response, expected_url)

    def test_initual_current_username_is_correct(self):
        response = self.client.get(reverse('authors:change_information'))

        content = response.content.decode()

        self.assertIn('value="testing"', content)

    def test_post_change_username_and_return_to_dashboard(self):
        users = User.objects.get()
        self.assertEqual(users.username, 'testing')

        response = self.client.post(
            reverse('authors:change_information'),
            data={
                'new_username': 'new_username'
            }
        )

        users = User.objects.get()
        self.assertEqual(users.username, 'new_username')

        # TODO switch to dashboard
        self.assertRedirects(response, reverse('home:index'))

    def test_wait_time_after_change_username_was_set_correctly(self):
        self.client.post(
            reverse('authors:change_information'),
            data={
                'new_username': 'new_username'
            }
        )

        response = self.client.get(
            reverse('authors:change_information'),
            follow=True
        )

        self.assertContains(response, const.CANNOT_CHANGE_USERNAME_ERROR)
        self.assertRedirects(response, reverse('home:index'))

    def test_can_change_username_after_7_days(self):
        self.client.post(
            reverse('authors:change_information'),
            data={
                'new_username': 'new_username'
            }
        )

        time_now = timezone.now()
        time_delta = timezone.timedelta(days=7)

        new_data = time_now - time_delta

        self.user.change_username_data = new_data
        self.user.save()

        response = self.client.get(
            reverse('authors:change_information'),
            follow=True
        )

        self.assertNotContains(response, const.CANNOT_CHANGE_USERNAME_ERROR)
        self.assertContains(response, const.USERNAMED_CHANGED_SUCCESS)

    # Override_settings in this test confirms that it will change the language.
    @override_settings(LANGUAGE_CODE='pt-br')
    def test_portuguese_translate_is_load_and_is_correct(self):
        activate('pt-br')

        response = self.client.get(reverse('authors:change_information'))
        self.assertContains(response, 'Seu nome de usuário atual:')
