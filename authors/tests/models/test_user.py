from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

User = get_user_model()


class UserModelTest(TestCase):
    def test_cannot_save_null_user(self):
        user = User(username=None)

        with self.assertRaises(IntegrityError):
            user.save()

    def test_cannot_save_empty_user(self):
        user = User(username='')

        with self.assertRaises(ValidationError):
            user.full_clean()
