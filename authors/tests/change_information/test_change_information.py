from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import resolve, reverse
from django.utils.translation import activate

import authors.constants as const
from authors.tests.helpers import create_user
from authors.utils import is_wait_time_done
from authors.views import ChangeInformationView

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

        self.assertEqual(response.func.view_class, ChangeInformationView)

    def test_view_load_correct_template(self):
        response = self.get_change_information()

        self.assertTemplateUsed(response, 'authors/pages/authors.html')

    def test_anonymous_user_cannot_get_the_page(self):
        self.client.logout()
        response = self.get_change_information()

        self.assertRedirects(response, reverse('authors:login'))

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

    def test_wait_time_after_change_username_was_set_correctly_use_GET(self):
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

    def test_wait_time_after_change_username_was_set_correctly_use_POST(self):
        self.client.post(
            reverse('authors:change_information'),
            data={
                'new_username': 'new_username'
            }
        )

        response = self.client.post(
            reverse('authors:change_information'),
            data={
                'new_username': 'new_username2'
            }, follow=True
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

        new_data = is_wait_time_done()

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
