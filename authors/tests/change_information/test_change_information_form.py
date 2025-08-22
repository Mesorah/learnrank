import lxml.html
from django.test import TestCase
from django.urls import reverse

from authors.forms import ChangeInformationForm
from authors.tests.helpers import create_user


class TestChangeInformationForm(TestCase):
    def test_renders_input_form(self):
        create_user(client=self.client, auto_login=True)

        response = self.client.get(reverse('authors:change_information'))
        parsed = lxml.html.fromstring(response.content)
        [form] = parsed.cssselect('form[method=POST]')

        self.assertEqual(
            form.get('action'), reverse('authors:change_information')
        )

        inputs_names = {
            'current_username': 'text',
            'new_username': 'text',
        }

        for input_name, expected_type in inputs_names.items():
            [input] = parsed.cssselect(f'input[name={input_name}]')

            self.assertEqual(input.get('type'), expected_type)

    def test_form_reand_only_is_active(self):
        create_user(client=self.client, auto_login=True)

        form = ChangeInformationForm()
        self.assertIn('readonly', form.fields['current_username'].widget.attrs)
