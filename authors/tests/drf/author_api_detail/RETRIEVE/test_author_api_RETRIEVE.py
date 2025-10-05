from django.contrib.auth import get_user_model

import utils.constants_informations as const_informations
from authors.tests.helpers import create_admin_user, create_user
from authors.tests.mixins_test import AuthorAPIMixin

User = get_user_model()


class AuthorAPIRETRIEVETest(AuthorAPIMixin):
    def setUp(self):
        self.user = create_user()

        return super().setUp()

    def test_user_without_permission_cannot_see_the_user_detail(self):
        other_user = create_user(username='other_user')

        response = self.get_authorized_view(
            self.request_author_api_detail, method='get',
            create_new_user=False, pk=other_user.pk
        )

        self.assertEqual(response.status_code, 403)

    def test_user_with_permission_can_see_the_user_detail(self):
        response = self.get_authorized_view(
            self.request_author_api_detail, method='get',
            create_new_user=False, pk=self.user.pk,
            username=self.user.username
        )

        self.assertEqual(response.status_code, 200)

    def test_admin_user_can_see_all_users_details(self):
        admin_user = create_admin_user()
        admin_password = const_informations.TEST_PASSWORD_ADMIN

        response = self.get_authorized_view(
            self.request_author_api_detail, method='get',
            create_new_user=False, pk=self.user.pk,
            username=admin_user.username, password=admin_password
        )

        self.assertEqual(response.status_code, 200)
