from urllib.parse import urlencode

from django.test import TestCase, override_settings
from django.urls import resolve, reverse
from django.utils.translation import activate

from authors.forms import CustomSignupForm
from authors.views import delete_author


class TestDeleteAuthor(TestCase):
    def setUp(self):
        form_data = {
            'username': 'testing',
            'email': 'testing@example.com',
            'password1': 'testing12!@1dsFG',
            'password2': 'testing12!@1dsFG',
        }

        form = CustomSignupForm(data=form_data)
        form.save()

        self.client.login(
            username='testing', password='testing12!@1dsFG'
        )

        return super().setUp()

    def test_view_is_correct(self):
        response = resolve(reverse('authors:delete'))

        self.assertEqual(response.func, delete_author)

    def test_view_load_correct_template(self):
        response = self.client.get(reverse('authors:delete'))

        self.assertTemplateUsed(
            response,
            'authors/pages/authors.html'
        )

    def test_get_view_returns_200(self):
        response = self.client.get(reverse('authors:delete'))

        self.assertEqual(response.status_code, 200)

    def test_user_not_authenticated_cant_get_200_in_delete(self):
        self.client.logout()

        response = self.client.get(reverse('authors:delete'))

        expected_url = (
            f"{reverse('authors:login')}"
            f"?{urlencode({'next': reverse('authors:delete')})}"
        )

        self.assertRedirects(response, expected_url)

        response = self.client.post(reverse('authors:delete'), data={
            'confirm': 'DELETE'
        }, follow=True)

        self.assertRedirects(response, expected_url)

        self.assertNotContains(
            response, 'Your account has been successfully deleted!'
        )

    # Override_settings in this test confirms that it will change the language.
    @override_settings(LANGUAGE_CODE='pt-br')
    def test_portuguese_translate_is_load_and_is_correct(self):
        activate('pt-br')

        response = self.client.get(reverse('authors:delete'))
        self.assertContains(response, 'Confirmação de exclusão da conta:')

        response = self.client.post(reverse('authors:delete'), data={
            'confirm': 'false'
        })

        content = response.content.decode()

        self.assertIn(
            'Confirmação incorreta. Por favor, digite &quot;DELETE&quot; '
            'para deletar sua conta.',
            content
        )

        response = self.client.post(reverse('authors:delete'), data={
            'confirm': 'DELETE'
        }, follow=True)

        self.assertContains(response, 'Sua conta foi excluída com sucesso!')
