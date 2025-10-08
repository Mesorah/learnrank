from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

import authors.constants as const
from authors.utils import change_username
from authors.validators import ChangeUsernameValidator

User = get_user_model()


class ChangeUsernameForm(forms.Form):
    current_username = forms.CharField(
        label=const.CURRENT_USERNAME_LABEL,
        required=False,
    )

    new_username = forms.CharField(
        label=const.NEW_USERNAME_LABEL,
        widget=forms.TextInput(
            attrs={'placeholder': const.NEW_USERNAME_PLACEHOLDER}
        )
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

        self.fields.get('current_username').initial = self.user.username

        self.fields.get('current_username').widget.attrs['readonly'] = True

    def get_new_username(self, super_clean, field):
        return super_clean.get(field) or self.data.get(field, '')

    def clean(self):
        super_clean = super().clean()

        ChangeUsernameValidator(
            change_username_data=self.user.change_username_data,
            new_username=self.get_new_username(super_clean, 'new_username'),
            validation_error=ValidationError,
            is_staff=self.user.is_staff
        )

        return super_clean

    def save(self):
        return change_username(user=self.user, cleaned_data=self.cleaned_data)
