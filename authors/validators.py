import re

from django.contrib.auth import get_user_model

import authors.constants as const

User = get_user_model()


class AuthorValidator:
    def __init__(self, values, ValidationError, add_error=None, context=None):
        self.values = values
        self.ValidationError = ValidationError
        self.add_error = add_error
        self.context = context

        self.control()

    def validate_username(self, field_name, add_error=True):
        username = self.values['username']

        if len(username) <= 3:
            msg = const.USERNAME_MIN_LENGTH_ERROR

            if add_error:
                self.add_error(field_name, msg)
            else:
                raise self.ValidationError({field_name: msg})

        if User.objects.filter(username=username).exists():
            msg = const.USERNAME_TAKEN_ALREADY_ERROR

            if add_error:
                self.add_error(field_name, msg)
            else:
                raise self.ValidationError({field_name: msg})

        return username

    def validate_email(self, field_name, add_error=True):
        email = self.values['email']

        if User.objects.filter(email=email).exists():
            msg = const.EMAIL_ALREADY_REGISTERED_ERROR

            if add_error:
                self.add_error(field_name, msg)
            else:
                raise self.ValidationError({field_name: msg})

        return email

    def validate_password_rules(self, password, field_name, add_error=True):
        # Verify if password1 have [a-z] or [1-9] and don't have symbols
        if password and password.isalnum():
            msg = const.PASSWORD_MUST_CONTAIN_SYMBOLS_ERROR

            if add_error:
                self.add_error(field_name, msg)
            else:
                raise self.ValidationError({field_name: msg})

        # Verify if password1 don't have numbers [1-9]
        if not re.search(r'\d', password):
            msg = const.PASSWORD_MUST_CONTAIN_NUMBERS_ERROR

            if add_error:
                self.add_error(field_name, msg)
            else:
                raise self.ValidationError({field_name: msg})

        if not re.search(r'[A-Za-z]', password):
            msg = const.PASSWORD_MUST_CONTAIN_LETTERS_ERROR

            if add_error:
                self.add_error(field_name, msg)
            else:
                raise self.ValidationError({field_name: msg})

    def validate_form(self):
        password1 = self.values['password1']
        password2 = self.values['password2']

        if password1 != password2:
            self.add_error('password2', const.PASSWORDS_DO_NOT_MATCH_ERROR)

        self.validate_password_rules(password1, 'password1')

        return self.values

    def validate_serializer(self):
        password = self.values['password']

        self.validate_password_rules(password, 'password', add_error=False)

        return self.values

    def control(self):
        if self.context == 'form':
            self.validate_username('username')
            self.validate_email('email')
            self.validate_form()

        if self.context == 'serializer':
            self.validate_username('username', add_error=False)
            self.validate_email('email', add_error=False)
            self.validate_serializer()
