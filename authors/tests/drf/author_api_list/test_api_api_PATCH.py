from django.urls import resolve, reverse

from authors.api import AuthorAPIDetail
from authors.tests.helpers import create_admin_user, create_user
from authors.tests.mixins_test import AuthorAPIMixin


class AuthorAPIPATCHTest(AuthorAPIMixin):
    def setUp(self):
        super().setUp()

        create_user(qtd=3)

        self.other_username = 'other'
        self.other_email = 'other@example.com'

        self.owner_username = 'owner'
        self.owner_email = 'owner@example.com'

        self.admin_password = 'testing12ADMIN!@1dsFG'

    def test_view_is_correct(self):
        response = resolve(reverse(
            'authors:author_api_detail', kwargs={'pk': '1'}
        ))

        self.assertEqual(response.func.view_class, AuthorAPIDetail)

    def test_user_not_logged_in_cannot_partial_update_author(self):
        response = self.request_author_api_detail(
            method='patch', pk='1', url='author_api_detail', data={
                'username': 'new_username'
            }
        )

        self.assertEqual(response.status_code, 401)

    def test_user_without_permission_cannot_partial_update_author(self):
        other_user = create_user(username='other', email='other@example.com')

        # pk is not owner user
        response = self.get_authorized_view(
            self.request_author_api_detail, method='patch',
            admin_user=False, pk=other_user.pk, data={
                'username': 'new_username'
            }
        )

        self.assertEqual(response.status_code, 403)

    def test_user_can_partial_update_account_when_owner(self):
        owner_user = create_user(
            username=self.owner_username, email=self.owner_email
        )

        response = self.get_authorized_view(
            self.request_author_api_detail, method='patch',
            username=self.owner_username, email=self.owner_email,
            create_new_user=False, pk=owner_user.pk,
            data={'username': 'new_username'}
        )

        self.assertEqual(response.status_code, 200)

    def test_user_can_partial_update_account_when_admin(self):
        owner_user = create_user(
            username=self.owner_username, email=self.owner_email
        )
        create_admin_user(
            username=self.other_username, email=self.other_email
        )

        # pk is not owner user
        response = self.get_authorized_view(
            self.request_author_api_detail, method='patch',
            username=self.other_username, email=self.other_email,
            password=self.admin_password,
            create_new_user=False, pk=owner_user.pk,
            data={'username': 'new_username'}
        )

        self.assertEqual(response.status_code, 200)

    def test_user_can_partial_update_account_when_admin_and_owner(self):
        admin_owner = create_admin_user(
            username=self.owner_username, email=self.owner_email
        )

        response = self.get_authorized_view(
            self.request_author_api_detail, method='patch',
            username=self.owner_username, email=self.owner_email,
            password=self.admin_password,
            create_new_user=False, pk=admin_owner.pk,
            data={'username': 'new_username'}
        )

        self.assertEqual(response.status_code, 200)

    # user tem que esperar o tempo para mudar de nome
