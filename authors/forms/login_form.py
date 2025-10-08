from django.contrib.auth.forms import AuthenticationForm

import authors.constants as const


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = (
            const.USERNAME_PLACEHOLDER
        )
        self.fields['password'].widget.attrs['placeholder'] = (
            const.PASSWORD_PLACEHOLDER
        )
