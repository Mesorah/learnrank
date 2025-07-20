from django.core import mail
from django.test import TestCase, override_settings
from django.urls import resolve, reverse
from django.utils.translation import activate

from authors.forms import CustomSignupForm
from authors.views import PasswordResetAuthorView


class TestPasswordResetAuthor(TestCase):
    def setUp(self):
        self.form_data = {
            'username': 'testing',
            'email': 'testing@example.com',
            'password1': 'testing12!@1dsFG',
            'password2': 'testing12!@1dsFG',
        }

        form = CustomSignupForm(data=self.form_data)
        form.save()

        self.user = self.client.login(
            username='testing', password='testing12!@1dsFG'
        )

        return super().setUp()

    def test_view_is_correct(self):
        response = resolve(reverse('authors:password_reset'))

        self.assertEqual(response.func.view_class, PasswordResetAuthorView)

    def test_view_load_correct_template(self):
        response = self.client.get(reverse('authors:password_reset'))

        self.assertTemplateUsed(
            response,
            'authors/pages/password_reset.html'
        )

    def test_get_view_returns_200(self):
        response = self.client.get(reverse('authors:password_reset'))

        self.assertEqual(response.status_code, 200)

    def test_email_was_sent_correctly(self):
        url = reverse('authors:password_reset')
        self.client.post(url, {'email': self.form_data['email']})

        email = mail.outbox

        self.assertEqual(len(email), 1)

        self.assertEqual(email[0].to, ['testing@example.com'])

        self.assertIn(
            ("You're receiving this email because you requested a password "
             "reset for your user account at"),
            email[0].body
        )

    def test_incorrect_email_was_not_sent(self):
        url = reverse('authors:password_reset')
        self.client.post(url, {'email': 'falseemail@example.com'})

        email = mail.outbox

        self.assertEqual(len(email), 0)

    def test_user_not_authenticated_cant_get_200_in_signup(self):
        self.client.logout()

        url = reverse('authors:password_reset')
        response = self.client.get(
            url, {'email': self.form_data['email']}, follow=True
        )

        self.assertRedirects(response, reverse('home:index'))
        self.assertContains(
            response, 'You cannot access this while not logged in.'
        )

    # Override_settings in this test confirms that it will change the language.
    @override_settings(LANGUAGE_CODE='pt-br')
    def test_portuguese_translate_is_load_and_is_correct(self):
        activate('pt-br')

        response = self.client.get(reverse('authors:password_reset'))
        self.assertContains(response, 'Enviar')

        url = reverse('authors:password_reset')
        self.client.post(url, {'email': self.form_data['email']})

        email = mail.outbox

        self.assertEqual(len(email), 1)

        self.assertEqual(email[0].to, ['testing@example.com'])

        self.assertIn(
            ('Você está recebendo este e-mail porque solicitou a redefinição '
             'de senha da sua conta no site'),
            email[0].body
        )
