from django.contrib.auth import get_user_model
from django.urls import resolve, reverse

from authors.api import AuthorAPIList
from authors.tests.mixins_test import AuthorAPIMixin

User = get_user_model()


class AuthorAPIPOSTTest(AuthorAPIMixin):
    def test_view_is_correct(self):
        response = resolve(reverse('authors:author_api_list'))

        self.assertEqual(response.func.view_class, AuthorAPIList)

    def test_user_without_permission_cannot_create_user(self):
        response = self.request_author_api_list(
            data={**self.data}, method='post'
        )

        self.assertEqual(response.status_code, 401)

    def test_user_with_permission_receives_error_without_values(self):
        response = self.get_authorized_view(
            self.request_author_api_list, method='post',
            admin_user=False
        )

        self.assertIn('This field is required.', response.data['username'])

        response = self.get_authorized_view(
            self.request_author_api_list, method='post',
            admin_user=False, username='test'
        )

        self.assertIn('This field is required.', response.data['email'])

    def test_user_with_permission_can_create_user(self):
        # username changed to avoid conflict with our user
        response = self.get_authorized_view(
            self.request_author_api_list, method='post',
            username='testing2', email='testing2@example.com',
            admin_user=False, data={**self.data}
        )

        self.assertEqual(response.status_code, 201)
