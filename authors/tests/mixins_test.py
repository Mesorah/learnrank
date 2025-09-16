from django.urls import reverse
from rest_framework.test import APITestCase

from authors.tests.helpers import create_admin_user, create_user


class AuthorAPIMixin(APITestCase):
    def setUp(self):
        self.data = {
            'username': 'testing',
            'email': 'testing@example.com',
            'password': 'testing12!@1dsFG',
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

    def request_author_api_list(self, method='get', *args, **kwargs):
        return getattr(self.client, method)(reverse(
            'authors:author_api_list'
        ), *args, **kwargs)

    def get_authorized_view(
        self,
        view_func,
        method='get',
        admin_user=True,
        username='testing',
        password='testing12!@1dsFG',
        email='testing@example.com',
        *args, **kwargs
    ):
        data = {
            'username': username,
            'email': email,
            'password': password,
        }

        """
        If the user wants to be an admin, call the admin function,
        otherwise create the user without admin.
        """
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
            HTTP_AUTHORIZATION='Bearer ' + access_token,
            *args, **kwargs
        )
