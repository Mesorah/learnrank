from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

import authors.constants as const


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['new_password1'].help_text = ''
        self.fields['new_password2'].help_text = ''

        self.fields['new_password1'].widget.attrs['placeholder'] = (
            const.NEW_PASSWORD1_PLACEHOLDER
        )

        self.fields['new_password2'].widget.attrs['placeholder'] = (
            const.NEW_PASSWORD2_PLACEHOLDER
        )


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['placeholder'] = (
            const.EMAIL_PLACEHOLDER
        )
