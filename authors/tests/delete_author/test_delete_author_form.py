import lxml.html
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import html

import authors.constants as consts
from authors.forms import CustomSignupForm

User = get_user_model()


class TestDeleteAuthorForm(TestCase):
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

    def test_confirm_validator_is_correct(self):
        response = self.client.post(reverse('authors:delete'), data={
            'confirm': 'false'
        })

        self.assertContains(
            response,
            html.escape(consts.DELETE_ACCOUNT_ERROR)
        )

    def test_post_delete_user_and_redirects_to_home(self):
        user = User.objects.filter(username='testing').exists()
        self.assertTrue(user)

        response = self.client.post(reverse('authors:delete'), data={
            'confirm': 'DELETE'
        }, follow=True)

        user = User.objects.filter(username='testing').exists()
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

        [input] = form.cssselect(f'input[name={'confirm'}]')
        self.assertEqual(input.get('type'), 'text')
