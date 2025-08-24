import lxml.html
from django.test import TestCase
from django.urls import reverse

import authors.constants as const
from authors.forms import ChangeUsernameForm
from authors.tests.helpers import create_user


class TestChangeUsernameForm(TestCase):
    # TODO create a helper to create_user

    def test_renders_input_form(self):
        create_user(client=self.client, auto_login=True)

        response = self.client.get(reverse('authors:change_username'))
        parsed = lxml.html.fromstring(response.content)
        [form] = parsed.cssselect('form[method=POST]')

        self.assertEqual(
            form.get('action'), reverse('authors:change_username')
        )

        inputs_names = {
            'current_username': 'text',
            'new_username': 'text',
        }

        for input_name, expected_type in inputs_names.items():
            [input] = parsed.cssselect(f'input[name={input_name}]')

            self.assertEqual(input.get('type'), expected_type)

    def test_form_reand_only_is_active(self):
        user = create_user(client=self.client, auto_login=True)

        form = ChangeUsernameForm(user)
        self.assertIn('readonly', form.fields['current_username'].widget.attrs)

    def test_form_is_correct(self):
        user = create_user(client=self.client, auto_login=True)

        form = ChangeUsernameForm(user=user, data={
            'new_username': 'new_username'
        })

        self.assertTrue(form.is_valid())

    def test_form_username_already_taken(self):
        create_user(client=self.client)
        user = create_user(
            client=self.client, username='testing2', auto_login=True
        )

        form = ChangeUsernameForm(user=user, data={
            'new_username': 'testing'
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['new_username'][0], const.USERNAME_TAKEN_ALREADY_ERROR
        )
