from django.contrib.auth import get_user_model

import authors.constants as const
from authors.serializers import AuthorSerializer
from authors.tests.mixins_test import AuthorAPIMixin

User = get_user_model()


class AuthorAPIValidatorsTest(AuthorAPIMixin):
    def test_username_validator_is_correct(self):
        self.data['username'] = 'abc'
        serializer = AuthorSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['username'][0], const.USERNAME_MIN_LENGTH_ERROR
        )

        self.data['username'] = 'abcd'
        serializer = AuthorSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        # Username already in use
        self.data['username'] = 'abcd'
        serializer = AuthorSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['username'][0],
            const.USERNAME_TAKEN_ALREADY_ERROR
        )

    def test_email_validator_is_correct(self):
        serializer = AuthorSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        # Email already in use
        self.data['username'] = 'testing2'
        serializer = AuthorSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['email'][0], const.EMAIL_ALREADY_REGISTERED_ERROR
        )

    def test_password_validator_is_correct(self):
        self.data['password'] = '12345678'
        serializer = AuthorSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            const.PASSWORD_MUST_CONTAIN_SYMBOLS_ERROR,
            serializer.errors['password']
        )

        self.data['password'] = '12345678!'
        serializer = AuthorSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            const.PASSWORD_MUST_CONTAIN_LETTERS_ERROR,
            serializer.errors['password']
        )

        self.data['password'] = 'ab@cdefgh'
        serializer = AuthorSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            const.PASSWORD_MUST_CONTAIN_NUMBERS_ERROR,
            serializer.errors['password']
        )

        self.data['password'] = 'abcdef1!'
        serializer = AuthorSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

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

        self.data['username'] = 'testing'
        self.data['email'] = 'testing@example.com'
        serializer = AuthorSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        self.assertEqual(User.objects.count(), 2)
