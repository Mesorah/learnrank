import lxml.html
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import html

import authors.constants as consts
import utils.constants_informations as const_informations
from authors.tests.helpers import create_user

User = get_user_model()


class TestDeleteAuthorForm(TestCase):
    def setUp(self):
        create_user(client=self.client, auto_login=True)

        return super().setUp()

    def test_confirm_validator_is_correct(self):
        response = self.client.post(reverse('authors:delete'), data={
            'confirm': 'false'
        })

        self.assertContains(
            response,
            html.escape(consts.DELETE_ACCOUNT_ERROR)
        )

    def test_post_delete_user_and_redirects_to_home(self):
        user = User.objects.filter(
            username=const_informations.TEST_USERNAME
        ).exists()
        self.assertTrue(user)

        response = self.client.post(reverse('authors:delete'), data={
            'confirm': 'DELETE'
        }, follow=True)

        user = User.objects.filter(
            username=const_informations.TEST_USERNAME
        ).exists()
        self.assertFalse(user)
        self.assertRedirects(response, reverse('home:index'))
        self.assertContains(
            response, consts.ACCOUNT_DELETED_SUCCESS
        )

    def test_renders_input_form(self):
        response = self.client.get(reverse('authors:delete'))
        parsed = lxml.html.fromstring(response.content)  # HTML -> DOM
        [form] = parsed.cssselect('form[method=POST]')  # -> Search a form
        self.assertEqual(form.get('action'), reverse('authors:delete'))

        [input] = form.cssselect(f"input[name={'confirm'}]")
        self.assertEqual(input.get('type'), 'text')
