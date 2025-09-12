from django.urls import reverse
from rest_framework.test import APITestCase


class AuthorAPIMixin(APITestCase):
    def get_jwt_acess_token(self, username, password):
        response = self.client.post(
            reverse('authors:token_obtain_pair'),
            data={
                'username': username,
                'password': password
            }
        )

        return response.data['access']

    def get_api_list(self, *args, **kwargs):
        return self.client.get(reverse(
            'authors:author_api_list'
        ), *args, **kwargs)
