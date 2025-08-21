import lxml.html
from django.test import TestCase
from django.urls import resolve, reverse

from authors.views import change_information


class TestChangeInformationForm(TestCase):
    def test_renders_input_form(self):
        response = self.client.get(reverse('authors:change_information'))
        parsed = lxml.html.fromstring(response.content)
        [form] = parsed.cssselect('form[method=POST]')

        self.assertEqual(
            form.get('action'), reverse('authors:change_information')
        )

        inputs_names = {
            'actual_username': 'text',
            'new_username': 'text',
        }

        for input_name, expected_type in inputs_names.items():
            [input] = parsed.cssselect(f'input[name={input_name}]')

            self.assertEqual(input.get('type'), expected_type)