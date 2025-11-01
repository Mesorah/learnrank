import re

from django.contrib.auth import get_user_model

import authors.constants as const
from authors.utils import is_wait_time_done

User = get_user_model()


class AuthorValidatorMixin:
    def validate_username_length(self, field_name, username):
        if len(username) <= 3:
            msg = const.USERNAME_MIN_LENGTH_ERROR

            raise self.validation_error({field_name: msg})

        return username

    def validade_username_already_exists(self, field_name, username):
        if User.objects.filter(username=username).exists():
            msg = const.USERNAME_ALREADY_TAKEN_ERROR

            raise self.validation_error({field_name: msg})

        return username

    def validate_email(self, field_name, email, add_error=True):
        if User.objects.filter(email=email).exists():
            msg = const.EMAIL_ALREADY_REGISTERED_ERROR

            if add_error:
                self.add_error(field_name, msg)
            else:
                raise self.validation_error({field_name: msg})

        return email

    def validate_password_rules(self, field_name, password, add_error=True):
        # Verify if password1 have [a-z] or [1-9] and don't have symbols
        if password and password.isalnum():
            msg = const.PASSWORD_MUST_CONTAIN_SYMBOLS_ERROR

            if add_error:
                self.add_error(field_name, msg)
            else:
                raise self.validation_error({field_name: msg})

        # Verify if password1 don't have numbers [1-9]
        if not re.search(r'\d', password):
            msg = const.PASSWORD_MUST_CONTAIN_NUMBERS_ERROR

            if add_error:
                self.add_error(field_name, msg)
            else:
                raise self.validation_error({field_name: msg})

        if not re.search(r'[A-Za-z]', password):
            msg = const.PASSWORD_MUST_CONTAIN_LETTERS_ERROR

            if add_error:
                self.add_error(field_name, msg)
            else:
                raise self.validation_error({field_name: msg})

        return password

    def validate_username_data(self, change_username_data, field_name):
        """
        Checks if the timeout for the user to rename their username has not
        ended, gets the time remaining to rename the username, and throws the
        error with the remaining time.
        """

        if (
            change_username_data is not None
            and
            # 25/10/2025 < 1/11/2025
            is_wait_time_done() < change_username_data
        ):
            # 1/11/2025 - 25/10/2025 -> 6 days and 23 hours
            time_to_wait = change_username_data - is_wait_time_done()

            # Because 7 days becomes 6 days and 23 hours.
            wait_days = time_to_wait.days + 1

            raise self.validation_error({
                field_name:
                const.CANNOT_CHANGE_USERNAME_ERROR % {'days': wait_days}
            })

        return change_username_data
