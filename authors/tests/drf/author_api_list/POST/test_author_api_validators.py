from django.contrib.auth import get_user_model

import authors.constants as const
import utils.constants_informations as const_informations
from authors.serializers import AuthorSerializer
from authors.tests.mixins_test import AuthorAPIMixin

User = get_user_model()


class AuthorAPIValidatorsTest(AuthorAPIMixin):
    def test_username_min_length_validator(self):
        self.data['username'] = 'abc'
        serializer = AuthorSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['username'][0], const.USERNAME_MIN_LENGTH_ERROR
        )

    def test_username_already_taken_validator(self):
        self.data['username'] = 'abcd'
        serializer = AuthorSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.data['username'] = 'abcd'
        serializer = AuthorSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['username'][0],
            const.USERNAME_ALREADY_TAKEN_ERROR
        )

    def test_email_already_registred_validator(self):
        serializer = AuthorSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.data['username'] = 'testing2'
        serializer = AuthorSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['email'][0], const.EMAIL_ALREADY_REGISTERED_ERROR
        )

    def test_password_min_length_validator(self):
        self.data['password'] = 'ab12!@'
        serializer = AuthorSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            const.PASSWORD1_MIN_LENGTH_ERROR,
            serializer.errors['password']
        )

    def test_password_must_contain_symbols_validator(self):
        self.data['password'] = '12345678a'
        serializer = AuthorSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            const.PASSWORD_MUST_CONTAIN_SYMBOLS_ERROR,
            serializer.errors['password']
        )

    def test_password_must_contain_letters_validator(self):
        self.data['password'] = '12345678!'
        serializer = AuthorSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            const.PASSWORD_MUST_CONTAIN_LETTERS_ERROR,
            serializer.errors['password']
        )

    def test_password_must_contain_numbers(self):
        self.data['password'] = 'ab@cdefgh'
        serializer = AuthorSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            const.PASSWORD_MUST_CONTAIN_NUMBERS_ERROR,
            serializer.errors['password']
        )

    def test_user_is_created(self):
        serializer = AuthorSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.assertEqual(User.objects.count(), 1)

        self.data['username'] = 'testing2'
        self.data['email'] = 'testing2@example.com'
        serializer = AuthorSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.assertEqual(User.objects.count(), 2)

        self.data['username'] = const_informations.TEST_USERNAME
        self.data['email'] = const_informations.TEST_EMAIL
        serializer = AuthorSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        self.assertEqual(User.objects.count(), 2)
