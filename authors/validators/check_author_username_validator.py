from .author_validator_mixin import AuthorValidatorMixin


class CheckAuthorUsernameValidator(AuthorValidatorMixin):
    def __init__(
            self, values, validation_error
    ):
        self.values = values
        self.validation_error = validation_error

        self.control()

    def control(self):
        self.validate_username_length(
            field_name='username', username=self.values['username'],
            add_error=False
        )
