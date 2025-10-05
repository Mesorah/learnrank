from django.urls import reverse

import utils.constants_informations as const_informations
from authors.tests.helpers import create_user
from authors.tests.mixins_test import AuthorAPIMixin


class AuthorAPICheckEmailTest(AuthorAPIMixin):
    def request_author_api_check_email(self, *args, **kwargs):
        return self.client.post(reverse(
            'authors:author_api_check_email'
        ), *args, **kwargs)

    def test_check_user_there_are_no_other_users_success(self):
        response = self.request_author_api_check_email(
            data={'email': const_informations.TEST_EMAIL}
        )

        self.assertFalse(response.data['email_already_registred'])

    def test_check_user_there_are_no_other_users_fail(self):
        response = self.request_author_api_check_email(
            data={'email': 'abc@example.com'}
        )

        self.assertFalse(response.data['email_already_registred'])

    def test_check_user_there_are_other_users_sucess(self):
        create_user(email='other_email@example.com')

        response = self.request_author_api_check_email(
            data={'email': const_informations.TEST_EMAIL}
        )

        self.assertFalse(response.data['email_already_registred'])

    def test_check_user_there_are_other_users_fail(self):
        create_user()

        response = self.request_author_api_check_email(
            data={'email': const_informations.TEST_EMAIL}
        )

        self.assertTrue(response.data['email_already_registred'])

    def test_user_did_not_submit_the_correct_field(self):
        response = self.request_author_api_check_email(
            data={'username': const_informations.TEST_USERNAME}
        )

        self.assertFalse(response.data['email_already_registred'])

        response = self.request_author_api_check_email(
            data={'password': const_informations.TEST_PASSWORD}
        )

        self.assertFalse(response.data['email_already_registred'])

    def test_user_sends_more_than_one_argument_success(self):
        response = self.request_author_api_check_email(
            data={
                'email': const_informations.TEST_EMAIL,
                'username': const_informations.TEST_USERNAME,
                'password': const_informations.TEST_PASSWORD
            }
        )

        self.assertFalse(response.data['email_already_registred'])
