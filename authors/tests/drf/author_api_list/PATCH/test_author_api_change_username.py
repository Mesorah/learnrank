from django.contrib.auth import get_user_model

import authors.constants as const
from authors.tests.helpers import change_username_data, create_user
from authors.tests.mixins_test import AuthorAPIMixin

User = get_user_model()


class AuthorAPIChangeUsernameTest(AuthorAPIMixin):
    def setUp(self):
        self.owner_username = 'owner'

        self.owner_user = create_user(username=self.owner_username)

        return super().setUp()

    def test_wait_time_after_change_username_was_set_correctly(self):
        # change first time
        self.change_username(
            username=self.owner_user.username,
            create_new_user=False, pk=self.owner_user.pk,
            new_username='new_username'
        )

        response = self.change_username(
            username=self.owner_user.username,
            create_new_user=False, pk=self.owner_user.pk,
            new_username='new_username2'
        )

        self.assertIn(
            const.CANNOT_CHANGE_USERNAME_ERROR % {'days': 7},
            response.data['new_username']
        )

    def test_can_change_username_after_7_days(self):
        # change first time
        self.change_username(
            username=self.owner_user.username,
            create_new_user=False, pk=self.owner_user.pk,
            new_username='new_username'
        )

        change_username_data(user=self.owner_user)

        response = self.change_username(
            username=self.owner_user.username,
            create_new_user=False, pk=self.owner_user.pk,
            new_username='new_username2'
        )

        self.assertEqual(response.status_code, 200)

    def test_username_change_wait_time_adjusts_after_repeated_changes(self):
        response = self.change_username(
            username=self.owner_user.username,
            create_new_user=False, pk=self.owner_user.pk,
            new_username='new_username'
        )

        change_username_data(user=self.owner_user, wait_days=2)

        response = self.change_username(
            username=self.owner_user.username,
            create_new_user=False, pk=self.owner_user.pk,
            new_username='new_username2'
        )

        self.assertIn(
            const.CANNOT_CHANGE_USERNAME_ERROR % {'days': 5},
            response.data['new_username']
        )

        change_username_data(user=self.owner_user, wait_days=4)

        response = self.change_username(
            username=self.owner_user.username,
            create_new_user=False, pk=self.owner_user.pk,
            new_username='new_username2'
        )

        self.assertIn(
            const.CANNOT_CHANGE_USERNAME_ERROR % {'days': 3},
            response.data['new_username']
        )
