import utils.constants_informations as const_informations
from authors.tests.helpers import create_admin_user, create_user
from authors.tests.mixins_test import AuthorAPIMixin


class AuthorAPIPUTTest(AuthorAPIMixin):
    def setUp(self):
        self.normal_user = create_user()
        self.admin_user = create_admin_user()
        self.admin_password = const_informations.TEST_PASSWORD_ADMIN

        return super().setUp()

    def test_method_PUT_is_unauthorized(self):
        response = self.request_author_api_detail(
            method='put', pk=self.normal_user.pk
        )

        self.assertEqual(response.status_code, 401)

    def test_method_PUT_is_forbidden(self):
        response = self.get_authorized_view(
            self.request_author_api_detail, method='put',
            create_new_user=False, username=self.normal_user.username,
            pk=self.normal_user.pk
        )

        self.assertEqual(response.status_code, 403)

    def test_method_PUT_is_not_allowed(self):
        response = self.get_authorized_view(
            self.request_author_api_detail, method='put',
            create_new_user=False, username=self.admin_user.username,
            password=self.admin_password, pk=self.admin_user.pk
        )

        self.assertEqual(response.status_code, 405)
