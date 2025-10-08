import authors.constants as const

from .author_validator_mixin import AuthorValidatorMixin


class AuthorPATCHValidator(AuthorValidatorMixin):
    def __init__(
            self, change_username_data, values, validation_error, is_staff
    ):
        self.values = values
        self.change_username_data = change_username_data
        self.validation_error = validation_error
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
            self, values, validation_error, add_error=None,
            context=None
    ):
        self.values = values
        self.validation_error = validation_error
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
