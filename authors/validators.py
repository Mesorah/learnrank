import re

from django.contrib.auth import get_user_model

import authors.constants as const
from authors.utils import is_wait_time_done

User = get_user_model()


class AuthorValidatorMixin:
    def validate_username_length(
            self, field_name, username, add_error=True
    ):
        if len(username) <= 3:
            msg = const.USERNAME_MIN_LENGTH_ERROR

            if add_error:
                self.add_error(field_name, msg)
            else:
                raise self.ValidationError({field_name: msg})

        return username

    def validade_username_already_exists(
            self, field_name, username, add_error=True
    ):
        if User.objects.filter(username=username).exists():
            msg = const.USERNAME_ALREADY_TAKEN_ERROR

            if add_error:
                self.add_error(field_name, msg)
            else:
                raise self.ValidationError({field_name: msg})

        return username

    def validate_email(self, field_name, email, add_error=True):
        if User.objects.filter(email=email).exists():
            msg = const.EMAIL_ALREADY_REGISTERED_ERROR

            if add_error:
                self.add_error(field_name, msg)
            else:
                raise self.ValidationError({field_name: msg})

        return email

    def validate_password_rules(self, field_name, password, add_error=True):
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

        return password

    def validate_username_data(self, change_username_data, field_name):
        if (
            change_username_data is not None
            and
            is_wait_time_done() < change_username_data
        ):

            time_to_wait = change_username_data - is_wait_time_done()

            # Because 7 days becomes 6 days and 23 hours.
            wait_days = time_to_wait.days + 1

            raise self.ValidationError({
                field_name:
                const.CANNOT_CHANGE_USERNAME_ERROR % {'days': wait_days}
            })


class ChangeUsernameValidator(AuthorValidatorMixin):
    def __init__(
        self, change_username_data, new_username, ValidationError, is_staff
    ):
        self.change_username_data = change_username_data
        self.new_username = new_username
        self.ValidationError = ValidationError
        self.is_staff = is_staff

        self.control()

    def control(self):
        self.validate_username_length(
            field_name='new_username', username=self.new_username,
            add_error=False
        )

        self.validade_username_already_exists(
            field_name='new_username', username=self.new_username,
            add_error=False
        )

        if not self.is_staff:
            self.validate_username_data(
                change_username_data=self.change_username_data,
                field_name='new_username'
            )


class AuthorPATCHValidator(AuthorValidatorMixin):
    def __init__(
            self, change_username_data, values, ValidationError, is_staff
    ):
        self.values = values
        self.change_username_data = change_username_data
        self.ValidationError = ValidationError
        self.is_staff = is_staff

        self.control()

    def control(self):
        if 'username' in self.values:
            if not self.is_staff:
                self.validate_username_data(
                    change_username_data=self.change_username_data,
                    field_name='new_username'
                )

            self.validate_username_length(
                field_name='new_username', username=self.values['username'],
                add_error=False
            )

            self.validade_username_already_exists(
                field_name='new_username', username=self.values['username'],
                add_error=False
            )

        if 'email' in self.values:
            self.validate_email(
                field_name='email', email=self.values['email'],
                add_error=False
            )

        if 'password' in self.values:
            self.validate_password_rules(
                field_name='password', password=self.values['password'],
                add_error=False
            )


class AuthorValidator(AuthorValidatorMixin):
    def __init__(
            self, values, ValidationError, add_error=None,
            context=None
    ):
        self.values = values
        self.ValidationError = ValidationError
        self.add_error = add_error
        self.context = context

        self.control()

    def validate_form(self):
        password1 = self.values['password1']
        password2 = self.values['password2']

        if password1 != password2:
            self.add_error('password2', const.PASSWORDS_DO_NOT_MATCH_ERROR)

        self.validate_password_rules(
            field_name='password1', password=password1
        )

        return self.values

    def validate_serializer(self):
        password = self.values['password']

        self.validate_password_rules(
            field_name='password', password=password, add_error=False
        )

        return self.values

    def control(self):
        if self.context == 'form':
            self.validate_username_length(
                field_name='username', username=self.values['username'],
                add_error=False
            )

            self.validade_username_already_exists(
                field_name='username', username=self.values['username'],
                add_error=False
            )
            self.validate_email('email', email=self.values['email'])
            self.validate_form()

        if self.context == 'serializer':
            self.validate_username_length(
                field_name='username', username=self.values['username'],
                add_error=False
            )

            self.validade_username_already_exists(
                field_name='username', username=self.values['username'],
                add_error=False
            )
            self.validate_email(
                'email', email=self.values['email'], add_error=False
            )
            self.validate_serializer()


class CheckAuthorUsernameValidator(AuthorValidatorMixin):
    def __init__(
            self, values, ValidationError
    ):
        self.values = values
        self.ValidationError = ValidationError

        self.control()

    def control(self):
        self.validate_username_length(
            field_name='username', username=self.values['username'],
            add_error=False
        )
