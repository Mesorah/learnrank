from django.contrib.auth import get_user_model

import authors.constants as const
from authors.tests.helpers import create_user
from authors.tests.mixins_test import AuthorAPIMixin

User = get_user_model()


class AuthorAPIValidatorsTest(AuthorAPIMixin):
    def setUp(self):
        self.owner_user = create_user()
        self.another_user = create_user(
            username='another_user', email='another_user@gmail.com'
        )

        return super().setUp()

    def test_email_validator(self):
        response = self.get_authorized_view(
            self.request_author_api_detail, method='patch',
            create_new_user=False, username=self.owner_user.username,
            pk=self.owner_user.pk, data={'email': self.another_user.email}
        )

        self.assertIn(
            const.EMAIL_ALREADY_REGISTERED_ERROR,
            response.data['email']
        )

    def test_password_validator_must_contain_symbols_error(self):
        response = self.get_authorized_view(
            self.request_author_api_detail, method='patch',
            create_new_user=False, username=self.owner_user.username,
            pk=self.owner_user.pk, data={'password': '12345678'}
        )
        self.assertIn(
            const.PASSWORD_MUST_CONTAIN_SYMBOLS_ERROR,
            response.data['password']
        )

    def test_password_validator_must_contain_letters_error(self):
        response = self.get_authorized_view(
            self.request_author_api_detail, method='patch',
            create_new_user=False, username=self.owner_user.username,
            pk=self.owner_user.pk, data={'password': '12345678!'}
        )
        self.assertIn(
            const.PASSWORD_MUST_CONTAIN_LETTERS_ERROR,
            response.data['password']
        )

    def test_password_validator_must_contain_numbers_error(self):
        response = self.get_authorized_view(
            self.request_author_api_detail, method='patch',
            create_new_user=False, username=self.owner_user.username,
            pk=self.owner_user.pk, data={'password': 'ab@cdefgh'}
        )
        self.assertIn(
            const.PASSWORD_MUST_CONTAIN_NUMBERS_ERROR,
            response.data['password']
        )
