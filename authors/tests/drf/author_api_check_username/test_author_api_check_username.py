from django.urls import reverse

from authors.tests.helpers import create_user
from authors.tests.mixins_test import AuthorAPIMixin


class AuthorAPICheckUsernameTest(AuthorAPIMixin):
    def request_author_api_check_username(self, *args, **kwargs):
        return self.client.post(reverse(
            'authors:author_api_check_username'
        ), *args, **kwargs)

    def test_check_user_there_are_no_other_users_success(self):
        response = self.request_author_api_check_username(
            data={'username': 'testing'}
        )

        self.assertTrue(response.data['success'])

    def test_check_user_there_are_no_other_users_fail(self):
        response = self.request_author_api_check_username(
            data={'username': 'abc'}
        )

        self.assertFalse(response.data['success'])

    def test_check_user_there_are_other_users_sucess(self):
        create_user(username='other_username')

        response = self.request_author_api_check_username(
            data={'username': 'testing'}
        )

        self.assertTrue(response.data['success'])

    def test_check_user_there_are_other_users_fail(self):
        create_user()

        response = self.request_author_api_check_username(
            data={'username': 'testing'}
        )

        self.assertFalse(response.data['success'])

    def test_user_did_not_submit_the_correct_field(self):
        response = self.request_author_api_check_username(
            data={'email': 'testing@example.com'}
        )

        self.assertFalse(response.data['success'])

        response = self.request_author_api_check_username(
            data={'password': 'testing12!@1dsFG'}
        )

        self.assertFalse(response.data['success'])

    def test_user_sends_more_than_one_argument_success(self):
        response = self.request_author_api_check_username(
            data={
                'username': 'testing',
                'email': 'testing@example.com',
                'password': 'testing12!@1dsFG'
            }
        )

        self.assertTrue(response.data['success'])
