from django.urls import resolve, reverse

from authors.api import AuthorAPIDetail
from authors.tests.helpers import create_admin_user, create_user
from authors.tests.mixins_test import AuthorAPIMixin


class AuthorAPIPATCHTest(AuthorAPIMixin):
    def setUp(self):
        super().setUp()

        create_user(qtd=3)

        self.another_username = 'other'
        self.another_email = 'other@example.com'

        self.owner_username = 'owner'
        self.owner_email = 'owner@example.com'

        self.admin_password = 'testing12ADMIN!@1dsFG'

        self.owner_user = create_user(
            username=self.owner_username,
            email=self.owner_email
        )

        self.another_user = create_user(
            username=self.another_username,
            email=self.another_email
        )

        self.admin_user = create_admin_user(password=self.admin_password)

    def test_view_is_correct(self):
        response = resolve(reverse(
            'authors:author_api_detail', kwargs={'pk': '1'}
        ))

        self.assertEqual(response.func.view_class, AuthorAPIDetail)

    def test_user_not_logged_in_cannot_partial_update_author_username(self):
        response = self.request_author_api_detail(
            method='patch', pk='1', url='author_api_detail', data={
                'username': 'new_username'
            }
        )

        self.assertEqual(response.status_code, 401)

    def test_user_without_permission_cannot_partial_update_author_name(self):
        # pk is not owner user
        response = self.get_authorized_view(
            self.request_author_api_detail, method='patch',
            admin_user=False, pk=self.another_user.pk, data={
                'username': 'new_username'
            }
        )

        self.assertEqual(response.status_code, 403)

    def test_user_can_partial_update_account_username_when_owner(self):
        response = self.get_authorized_view(
            self.request_author_api_detail, method='patch',
            username=self.owner_username, email=self.owner_email,
            create_new_user=False, pk=self.owner_user.pk,
            data={'username': 'new_username'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'new_username')

    def test_user_can_partial_update_account_username_when_admin(self):
        # pk is not owner user
        response = self.get_authorized_view(
            self.request_author_api_detail, method='patch',
            username=self.admin_user.username, email=self.admin_user.email,
            password=self.admin_password,
            create_new_user=False, pk=self.another_user.pk,
            data={'username': 'new_username'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'new_username')

    def test_user_can_partial_update_account_name_when_admin_and_owner(self):
        response = self.get_authorized_view(
            self.request_author_api_detail, method='patch',
            username=self.admin_user.username, email=self.admin_user.email,
            password=self.admin_password,
            create_new_user=False, pk=self.admin_user.pk,
            data={'username': 'new_username'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'new_username')

    def test_user_not_logged_in_cannot_partial_update_author_email(self):
        response = self.request_author_api_detail(
            method='patch', pk=self.another_user.pk,
            url='author_api_detail', data={
                'email': 'new_email'
            }
        )

        self.assertEqual(response.status_code, 401)

    def test_user_without_permission_cannot_partial_update_author_email(self):
        response = self.get_authorized_view(
            self.request_author_api_detail, method='patch',
            create_new_user=False, username=self.another_user.username,
            pk=self.owner_user.pk, data={'email': 'new_email@gamil.com'}
        )

        self.assertEqual(response.status_code, 403)

    def test_user_can_partial_update_account_email_when_owner(self):
        response = self.get_authorized_view(
            self.request_author_api_detail, method='patch',
            create_new_user=False, username=self.owner_user.username,
            pk=self.owner_user.pk, data={'email': 'new_email@gmail.com'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'new_email@gmail.com')

    def test_user_can_partial_update_account_email_when_admin(self):
        response = self.get_authorized_view(
            self.request_author_api_detail, method='patch',
            username=self.admin_user.username, email=self.admin_user.email,
            password=self.admin_password,
            create_new_user=False, pk=self.another_user.pk,
            data={'email': 'new_email@gmail.com'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'new_email@gmail.com')

    def test_user_can_partial_update_account_email_when_admin_and_owner(self):
        response = self.get_authorized_view(
            self.request_author_api_detail, method='patch',
            username=self.admin_user.username, email=self.admin_user.email,
            password=self.admin_password,
            create_new_user=False, pk=self.admin_user.pk,
            data={'email': 'new_email@gmail.com'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'new_email@gmail.com')

    def test_user_not_logged_in_cannot_partial_update_author_password(self):
        response = self.request_author_api_detail(
            method='patch', pk=self.another_user.pk,
            url='author_api_detail', data={
                'password': 'abcdef1!'
            }
        )

        self.assertEqual(response.status_code, 401)

    def test_user_without_permission_cannot_partial_update_password(self):
        response = self.get_authorized_view(
            self.request_author_api_detail, method='patch',
            create_new_user=False, username=self.another_user.username,
            pk=self.owner_user.pk, data={'password': 'abcdef1!'}
        )

        self.assertEqual(response.status_code, 403)

    def test_user_can_partial_update_account_password_when_owner(self):
        response = self.get_authorized_view(
            self.request_author_api_detail, method='patch',
            create_new_user=False, username=self.owner_user.username,
            pk=self.owner_user.pk, data={'password': 'abcdef1!'}
        )

        self.assertEqual(response.status_code, 200)

    def test_user_can_partial_update_account_password_when_admin(self):
        response = self.get_authorized_view(
            self.request_author_api_detail, method='patch',
            username=self.admin_user.username, email=self.admin_user.email,
            password=self.admin_password,
            create_new_user=False, pk=self.another_user.pk,
            data={'password': 'abcdef1!'}
        )

        self.assertEqual(response.status_code, 200)

    def test_user_can_partial_update_password_when_admin_and_owner(self):
        response = self.get_authorized_view(
            self.request_author_api_detail, method='patch',
            username=self.admin_user.username, email=self.admin_user.email,
            password=self.admin_password,
            create_new_user=False, pk=self.admin_user.pk,
            data={'password': 'abcdef1!'}
        )

        self.assertEqual(response.status_code, 200)
