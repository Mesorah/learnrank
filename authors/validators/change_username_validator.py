from .author_validator_mixin import AuthorValidatorMixin


class ChangeUsernameValidator(AuthorValidatorMixin):
    def __init__(
        self, change_username_data, new_username, validation_error, is_staff
    ):
        self.change_username_data = change_username_data
        self.new_username = new_username
        self.validation_error = validation_error
        self.is_staff = is_staff

        self.control()

    def control(self):
        self.validate_username_length(
            field_name='new_username', username=self.new_username,
        )

        self.validade_username_already_exists(
            field_name='new_username', username=self.new_username,
        )

        if not self.is_staff:
            self.validate_username_data(
                change_username_data=self.change_username_data,
                field_name='new_username'
            )
