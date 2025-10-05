from django.urls import reverse
from rest_framework.test import APITestCase

import utils.constants_informations as const_informations
from authors.tests.helpers import create_admin_user, create_user


class AuthorAPIMixin(APITestCase):
    def setUp(self):
        self.password = const_informations.TEST_PASSWORD

        self.data = {
            'username': const_informations.TEST_USERNAME,
            'email': const_informations.TEST_EMAIL,
            'password': self.password,
        }

        return super().setUp()

    def get_jwt_acess_token(self, username, password):
        response = self.client.post(
            reverse('authors:token_obtain_pair'),
            data={
                'username': username,
                'password': password
            }
        )

        return response.data['access']

    def request_author_api_list(self, method, page=1, *args, **kwargs):
        return getattr(self.client, method)(reverse(
            'authors:author_api_list'
        ) + f'?page={page}', *args, **kwargs)

    def request_author_api_detail(self, method, pk, *args, **kwargs):
        return getattr(self.client, method)(reverse(
            'authors:author_api_detail', kwargs={'pk': pk}
        ), *args, **kwargs)

    def change_username(
        self, username, create_new_user, pk,
        new_username, password=None
    ):
        if password is None:
            password = self.password

        return self.get_authorized_view(
            self.request_author_api_detail, method='patch',
            username=username, password=password,
            create_new_user=create_new_user, pk=pk,
            data={'username': new_username}
        )

    def get_authorized_view(
        self,
        view_func,
        method='get',
        pk=None,
        create_new_user=True,
        admin_user=True,
        *args, **kwargs
    ):
        username = kwargs.get('username', const_informations.TEST_USERNAME)
        email = kwargs.get('email', const_informations.TEST_EMAIL)
        password = kwargs.get('password', const_informations.TEST_PASSWORD)

        data = {
            'username': username,
            'email': email,
            'password': password,
        }

        """
        If the user wants to be an admin, call the admin function,
        otherwise create the user without admin.
        """
        if create_new_user:
            create_admin_user(**data) if admin_user else create_user(**data)

        access_token = self.get_jwt_acess_token(
            username, password
        )

        """
        Return the function you want
        Ex:self.get_authorized_view(self.request_author_api_list, method='get')
        """
        return view_func(
            method=method,
            pk=pk,
            HTTP_AUTHORIZATION='Bearer ' + access_token,
            *args, **kwargs
        )
