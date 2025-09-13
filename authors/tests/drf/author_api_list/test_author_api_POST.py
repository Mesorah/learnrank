from django.urls import resolve, reverse

from authors.api import AuthorAPIList
from authors.tests.mixins_test import AuthorAPIMixin


class AuthorAPIPOSTTest(AuthorAPIMixin):
    def setUp(self):
        self.data = {
            'username': 'testing',
            'email': 'testing@example.com',
            'password': 'testing12!@1dsFG',
        }

        return super().setUp()

    def test_view_is_correct(self):
        response = resolve(reverse('authors:author_api_list'))

        self.assertEqual(response.func.view_class, AuthorAPIList)

    def test_user_without_permission_cannot_create_user(self):
        response = self.post_api_list(data={**self.data})

        self.assertEqual(response.status_code, 401)

    def test_user_with_permission_receives_error_without_values(self):
        response = self.get_authorized_view(
            self.post_api_list, admin_user=False
        )

        self.assertIn('This field is required.', response.data['username'])
        self.assertIn('This field is required.', response.data['email'])

    def test_user_with_permission_can_create_user(self):
        # username changed to avoid conflict with our user
        response = self.get_authorized_view(
            self.post_api_list, username='testing2', admin_user=False,
            data={**self.data}
        )

        self.assertEqual(response.status_code, 201)
