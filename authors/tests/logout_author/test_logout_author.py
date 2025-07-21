from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import resolve, reverse
from django.utils.translation import activate

from authors import views

User = get_user_model()


class TestLogoutAuthor(TestCase):
    def test_view_is_correct(self):
        response = resolve(reverse('authors:logout'))
        self.assertEqual(response.func, views.logout_author)

    def test_get_view_returns_405(self):
        response = self.client.get(reverse('authors:logout'))
        self.assertEqual(response.status_code, 405)

    def test_post_view_redirects_to_correct_url(self):
        user = User.objects.create(username='test')
        self.client.force_login(user=user)

        response = self.client.post(reverse('authors:logout'))

        self.assertRedirects(response, reverse('authors:login'))

    def test_anonymous_user_cannot_logout(self):
        response = self.client.post(reverse('authors:logout'), follow=True)

        messages = list(response.context['messages'])

        self.assertFalse(
            any(
                actual_message.message == 'Success, you have logged out!'
                for actual_message in messages
            )
        )

        expected_url = (
            f"{reverse('authors:login')}"
            f"?{urlencode({'next': reverse('authors:logout')})}"
        )

        self.assertRedirects(response, expected_url)

    def test_logged_out_user_can_access_auth_pages(self):
        user = User.objects.create(username='test')
        self.client.force_login(user=user)

        # Logged
        response = self.client.get(reverse('authors:signup'))
        self.assertRedirects(response, reverse('home:index'))

        # Not logged
        response = self.client.post(reverse('authors:logout'))
        self.assertRedirects(response, reverse('authors:login'))

    # Override_settings in this test confirms that it will change the language.
    @override_settings(LANGUAGE_CODE='pt-br')
    def test_portuguese_translate_message_is_correct(self):
        activate('pt-br')

        user = User.objects.create(username='test')
        self.client.force_login(user=user)
        response = self.client.post(reverse('authors:logout'), follow=True)
        messages = list(response.context['messages'])

        self.assertTrue(any(
            actual_message.message == 'Você saiu da conta com sucesso!'
            and
            actual_message.level == 25
            for actual_message in messages
        ))
