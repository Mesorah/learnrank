from django.urls import resolve, reverse

from authors.api import AuthorAPIList
from authors.tests.helpers import create_user
from authors.tests.mixins_test import AuthorAPIMixin


class AuthorAPIListTest(AuthorAPIMixin):
    def setUp(self):
        create_user(qtd=5)

        return super().setUp()

    def test_view_is_correct(self):
        response = resolve(reverse('authors:author_api_list'))

        self.assertEqual(response.func.view_class, AuthorAPIList)

    def test_user_without_permission_cannot_see_the_user_list(self):
        response = self.request_author_api_list(method='get')

        self.assertEqual(response.status_code, 401)

    def test_api_pagination(self):
        response = self.get_authorized_view(
            self.request_author_api_list, method='get',
            create_new_user=True, page=1
        )

        count = response.data.get('count')
        user_in_a_one_page = len(response.data.get('results'))

        self.assertEqual(user_in_a_one_page, 5)

        # Because get_authorized_view create a new user
        self.assertEqual(count, 6)

        response = self.get_authorized_view(
            self.request_author_api_list, method='get',
            create_new_user=False, page=2
        )
        user_in_a_one_page = len(response.data.get('results'))

        self.assertEqual(user_in_a_one_page, 1)
