from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.core.exceptions import ValidationError

import authors.constants as const
from authors.utils import change_username
from authors.validators import AuthorValidator, ChangeUsernameValidator

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
            ValidationError=ValidationError,
            is_staff=self.user.is_staff
        )

        return super_clean

    def save(self):
        return change_username(user=self.user, cleaned_data=self.cleaned_data)


class ConfirmForm(forms.Form):
    confirm = forms.CharField(
        label=const.DELETE_CONFIRMATION_LABEL,
        widget=forms.TextInput(
            attrs={'placeholder': const.DELETE_ACCOUNT_PLACEHOLDER}
        )
    )

    def clean_confirm(self):
        confirm = self.cleaned_data['confirm']

        if str(confirm) != 'DELETE':
            raise ValidationError(const.DELETE_ACCOUNT_ERROR)

        return confirm


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


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = (
            const.USERNAME_PLACEHOLDER
        )
        self.fields['password'].widget.attrs['placeholder'] = (
            const.PASSWORD_PLACEHOLDER
        )


class CustomSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 'email',
            'password1', 'password2'
        ]

    username = forms.CharField(
        label=const.USERNAME_LABEL,
        min_length=4,
        error_messages={
            'min_length': const.USERNAME_MIN_LENGTH_ERROR,
            'unique': const.USERNAME_TAKEN_ALREADY_ERROR
        },
        max_length=30, widget=forms.TextInput(
            attrs={'placeholder': const.SIGNUP_USERNAME_PLACEHOLDER}
        ),
    )
    email = forms.EmailField(
        label=const.EMAIL_LABEL,
        max_length=256, widget=forms.EmailInput(
            attrs={'placeholder': const.SIGNUP_EMAIL_PLACEHOLDER}
        )
    )
    password1 = forms.CharField(
        label=const.PASSWORD1_LABEL,
        min_length=8,
        error_messages={'min_length': const.PASSWORD1_MIN_LENGTH_ERROR},
        max_length=50, widget=forms.PasswordInput(
            attrs={'placeholder': const.SIGNUP_PASSWORD1_PLACEHOLDER}
        )
    )
    password2 = forms.CharField(
        label=const.PASSWORD2_LABEL,
        min_length=8,
        error_messages={'min_length': const.PASSWORD2_MIN_LENGTH_ERROR},
        max_length=50, widget=forms.PasswordInput(
            attrs={'placeholder': const.SIGNUP_PASSWORD2_PLACEHOLDER}
        )
    )

    def get_clean_data(self, super_clean):
        values = {}

        for field_name in ['username', 'email', 'password1', 'password2']:
            values[field_name] = (
                super_clean.get(field_name) or self.data.get(field_name, '')
            )

        return values

    def clean(self):
        super_clean = super().clean()

        AuthorValidator(
            values=self.get_clean_data(super_clean),
            ValidationError=ValidationError,
            add_error=self.add_error,
            context='form'
        )

        return super_clean

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
