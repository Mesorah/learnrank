from django.test import TestCase, override_settings
from django.urls import resolve, reverse
from django.utils import html
from django.utils.translation import activate

import authors.constants as const
from authors.views import DeleteAuthorView

from ..helpers import create_user


class TestDeleteAuthor(TestCase):
    def setUp(self):
        create_user(client=self.client, auto_login=True)

        return super().setUp()

    def test_view_is_correct(self):
        response = resolve(reverse('authors:delete'))

        self.assertEqual(response.func.view_class, DeleteAuthorView)

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

        self.assertRedirects(response, reverse('home:index'))

        response = self.client.post(reverse('authors:delete'), data={
            'confirm': 'DELETE'
        }, follow=True)

        self.assertRedirects(response, reverse('home:index'))

        self.assertNotContains(
            response, const.ACCOUNT_DELETED_SUCCESS
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
            html.escape(
                'Confirmação incorreta. Por favor, digite "DELETE" '
                'para deletar sua conta.'
            ),
            content
        )

        response = self.client.post(reverse('authors:delete'), data={
            'confirm': 'DELETE'
        }, follow=True)

        self.assertContains(response, 'Sua conta foi excluída com sucesso!')
