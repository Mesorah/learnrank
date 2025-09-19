from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import resolve, reverse
from django.utils.translation import activate

import authors.constants as const
from authors.tests.helpers import (  # noqa E501
    change_username_data,
    create_admin_user,
    create_user,
)
from authors.views import ChangeUsernameView

User = get_user_model()


class TestChangeUsername(TestCase):
    def setUp(self):
        self.user = create_user(client=self.client, auto_login=True)

        return super().setUp()

    def get_change_username(self):
        return self.client.get(reverse('authors:change_username'))

    def change_username(self, new_username_name='new_username', follow=False):
        return self.client.post(
            reverse('authors:change_username'),
            data={
                'new_username': new_username_name
            }, follow=True if follow else False
        )

    def test_view_is_correct(self):
        self.client.logout()
        response = resolve(reverse('authors:change_username'))

        self.assertEqual(response.func.view_class, ChangeUsernameView)

    def test_view_load_correct_template(self):
        response = self.get_change_username()

        self.assertTemplateUsed(response, 'authors/pages/authors.html')

    def test_anonymous_user_cannot_get_the_page(self):
        self.client.logout()
        response = self.get_change_username()

        self.assertRedirects(response, reverse('authors:login'))

    def test_initual_current_username_is_correct(self):
        response = self.client.get(reverse('authors:change_username'))

        content = response.content.decode()

        self.assertIn('value="testing"', content)

    def test_post_change_username_and_return_to_dashboard(self):
        users = User.objects.get()
        self.assertEqual(users.username, 'testing')

        response = self.change_username()

        users = User.objects.get()
        self.assertEqual(users.username, 'new_username')

        # TODO switch to dashboard
        self.assertRedirects(response, reverse('home:index'))

    def test_wait_time_after_change_username_was_set_correctly_use_POST(self):
        self.change_username()

        response = self.change_username(
            new_username_name='new_username2', follow=True
        )

        self.assertContains(
            response, const.CANNOT_CHANGE_USERNAME_ERROR % {'days': 7}
        )

    def test_can_change_username_after_7_days(self):
        self.change_username()

        change_username_data(self.user)

        response = self.change_username(
            new_username_name='testing2', follow=True
        )
        self.assertRedirects(response, reverse('home:index'))

        self.assertNotContains(response, const.CANNOT_CHANGE_USERNAME_ERROR)
        self.assertContains(response, const.USERNAMED_CHANGED_SUCCESS)

    def test_username_change_wait_time_adjusts_after_repeated_changes(self):
        self.change_username()

        change_username_data(self.user, wait_days=2)

        response = self.change_username(follow=True)

        self.assertContains(
            response, const.CANNOT_CHANGE_USERNAME_ERROR % {'days': 5}
        )

        change_username_data(self.user, wait_days=4)

        response = self.change_username(follow=True)

        self.assertContains(
            response, const.CANNOT_CHANGE_USERNAME_ERROR % {'days': 3}
        )

    def test_wait_time_not_work_in_admin_user(self):
        # logout of the account without being admin
        self.client.logout()

        create_admin_user(client=self.client, auto_login=True)

        response = self.change_username()

        response = self.change_username(
            new_username_name='new_username2', follow=True
        )

        self.assertNotContains(
            response, const.CANNOT_CHANGE_USERNAME_ERROR % {'days': 7}
        )

    # Override_settings in this test confirms that it will change the language.
    @override_settings(LANGUAGE_CODE='pt-br')
    def test_portuguese_translate_is_load_and_is_correct(self):
        activate('pt-br')

        response = self.client.get(reverse('authors:change_username'))
        self.assertContains(response, 'Seu nome de usuário atual:')
