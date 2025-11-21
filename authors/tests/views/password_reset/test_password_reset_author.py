from django.core import mail
from django.test import TestCase, override_settings
from django.urls import resolve, reverse
from django.utils.translation import activate

import utils.constants_informations as const_informations
from authors.tests.helpers import create_user
from authors.views import PasswordResetAuthorView


class TestPasswordResetAuthor(TestCase):
    def setUp(self):
        create_user(client=self.client, auto_login=True)

        self.email_data = const_informations.TEST_EMAIL

        self.url = reverse('authors:password_reset')

        return super().setUp()

    def test_view_is_correct(self):
        response = resolve(self.url)

        self.assertEqual(response.func.view_class, PasswordResetAuthorView)

    def test_view_load_correct_template(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'authors/pages/password_reset.html'
        )

    def test_get_view_returns_200(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_email_was_sent_correctly(self):
        self.client.post(self.url, {'email': self.email_data})

        email = mail.outbox

        self.assertEqual(len(email), 1)

        self.assertEqual(email[0].to, [const_informations.TEST_EMAIL])

        self.assertIn(
            ("You're receiving this email because you requested a password "
             "reset for your user account at"),
            email[0].body
        )

    def test_incorrect_email_was_not_sent(self):
        self.client.post(self.url, {'email': 'falseemail@example.com'})

        email = mail.outbox

        self.assertEqual(len(email), 0)

    # Override_settings in this test confirms that it will change the language.
    @override_settings(LANGUAGE_CODE='pt-br')
    def test_portuguese_translate_is_load_and_is_correct(self):
        activate('pt-br')

        response = self.client.get(reverse('authors:password_reset'))
        self.assertContains(response, 'Enviar')

        self.client.post(self.url, {'email': self.email_data})

        email = mail.outbox

        self.assertEqual(len(email), 1)

        self.assertEqual(email[0].to, [const_informations.TEST_EMAIL])

        self.assertIn(
            ('Você está recebendo este e-mail porque solicitou a redefinição '
             'de senha da sua conta no site'),
            email[0].body
        )
