from django.urls import resolve, reverse

from authors.api import author_api_list
from authors.tests.helpers import create_admin_user, create_user
from authors.tests.test_mixins import AuthorAPIMixin


class AuthorAPIListTest(AuthorAPIMixin):
    def setUp(self):
        create_user(users=3)

        return super().setUp()

    def test_view_is_correct(self):
        response = resolve(reverse('authors:author_api_list'))

        self.assertEqual(response.func, author_api_list)

    def test_user_without_permission_cannot_see_the_user_list(self):
        response = self.get_api_list()

        self.assertEqual(response.status_code, 401)

    def test_user_with_permission_can_see_the_user_list(self):
        admin_user = create_admin_user()

        access_token = self.get_jwt_acess_token(
            admin_user.username, 'testing12!@1dsFG'
        )

        response = self.get_api_list(
            HTTP_AUTHORIZATION='Bearer ' + access_token,
        )

        self.assertEqual(len(response.data), 4)
