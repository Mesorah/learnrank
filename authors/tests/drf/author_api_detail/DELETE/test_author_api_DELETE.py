from django.contrib.auth import get_user_model

import utils.constants_informations as const_informations
from authors.tests.helpers import create_admin_user, create_user
from authors.tests.mixins_test import AuthorAPIMixin

User = get_user_model()


class AuthorAPIDELETETest(AuthorAPIMixin):
    def setUp(self):
        self.admin_user = create_admin_user()
        self.normal_user = create_user()

        self.admin_password = const_informations.TEST_PASSWORD_ADMIN

        return super().setUp()

    def test_user_not_logged_in_delete_author(self):
        response = self.request_author_api_detail(
            method='delete', pk=self.normal_user.pk,
            url='author_api_detail', data={
                'confirm': 'DELETE'
            }
        )

        self.assertEqual(response.status_code, 401)

    def test_user_without_permission_cannot_delete_author(self):
        response = self.get_authorized_view(
            self.request_author_api_detail, method='delete',
            create_new_user=False, pk=self.admin_user.pk,
            username=self.normal_user.username, data={
                'confirm': 'DELETE'
            }
        )

        self.assertEqual(response.status_code, 403)

    def test_user_cannot_delete_account_when_owner(self):
        response = self.get_authorized_view(
            self.request_author_api_detail, method='delete',
            username=self.normal_user, create_new_user=False,
            pk=self.normal_user.pk, data={
                'confirm': 'DELETE'
            }
        )

        self.assertEqual(response.status_code, 403)

    def test_user_can_delete_account_when_admin(self):
        response = self.get_authorized_view(
            self.request_author_api_detail, method='delete',
            username=self.admin_user.username, password=self.admin_password,
            create_new_user=False, pk=self.normal_user.pk, data={
                'confirm': 'DELETE'
            }
        )

        self.assertEqual(response.status_code, 204)

    def test_user_can_delete_account_when_admin_and_owner(self):
        response = self.get_authorized_view(
            self.request_author_api_detail, method='delete',
            username=self.admin_user.username, password=self.admin_password,
            create_new_user=False, pk=self.admin_user.pk, data={
                'confirm': 'DELETE'
            }
        )

        self.assertEqual(response.status_code, 204)
