import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

import authors.constants as const

User = get_user_model()


class AuthorValidator:
    def __init__(self, values, ValidationError, add_error=None):
        self.values = values
        self.ValidationError = ValidationError
        self.add_error = (
            add_error if add_error else self.ValidationError
        )

        self.validate()

    def validate_username(self):
        username = self.values['username']

        if User.objects.filter(username=username).exists():
            raise self.ValidationError({
                'username': const.USERNAME_TAKEN_ALREADY_ERROR
            })

        return username

    def validate_email(self):
        email = self.values['email']

        if User.objects.filter(email=email).exists():
            raise self.ValidationError({
                'email': const.EMAIL_ALREADY_REGISTERED_ERROR
            })

        return email

    def validate(self):
        self.validate_username()
        self.validate_email()

        password1 = self.values['password1']
        password2 = self.values['password2']

        if password1 != password2:
            raise self.ValidationError({
                'password2': const.PASSWORDS_DO_NOT_MATCH_ERROR
            })

        # Verify if password1 have [a-z] or [1-9] and don't have symbols
        if password1 and password1.isalnum():
            self.add_error(
                'password1', const.PASSWORD_MUST_CONTAIN_SYMBOLS_ERROR
            )

        # Verify if password1 don't have numbers [1-9]
        if not re.search(r'\d', password1):
            self.add_error(
                'password1', const.PASSWORD_MUST_CONTAIN_NUMBERS_ERROR
            )

        if not re.search(r'[A-Za-z]', password1):
            self.add_error(
                'password1', const.PASSWORD_MUST_CONTAIN_LETTERS_ERROR
            )

        return self.values
