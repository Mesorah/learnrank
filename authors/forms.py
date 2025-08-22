import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.core.exceptions import ValidationError

import authors.constants as const

User = get_user_model()


class ChangeInformationForm(forms.Form):
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

    def save(self):
        user = User.objects.get(id=self.user.id)

        user.username = self.cleaned_data.get(
            'new_username', 'actual_username'
        )

        user.save()

    def clean_new_username(self):
        new_username = self.cleaned_data['new_username']

        if User.objects.filter(username=new_username).exists():
            raise ValidationError(const.USERNAME_TAKEN_ALREADY_ERROR)

        return new_username


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


class CustomSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'email',
            'password1', 'password2'
        ]

    username = forms.CharField(
        label=const.USERNAME_LABEL,
        min_length=4,
        error_messages={'min_length': const.USERNAME_MIN_LENGTH_ERROR},
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

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise ValidationError(const.USERNAME_TAKEN_ALREADY_ERROR)

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise ValidationError(const.EMAIL_ALREADY_REGISTERED_ERROR)

        return email

    def clean(self):
        cleaned_data = self.cleaned_data
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            self.add_error('password2', const.PASSWORDS_DO_NOT_MATCH_ERROR)

        # Verify if password1 have [a-z] or [1-9] and don't have symbols
        if password1 and password1.isalnum():
            self.add_error(
                'password1', const.PASSWORD_MUST_CONTAIN_SYMBOLS_ERROR
            )

        # Verify if password1 don't have numbers [1-9]
        if not re.search(r'\d', password1):
            self.add_error(
                'password1', const.PASSWORD_MUST_CONTAIN_NUMBERS_ERROR
            )

        if not re.search(r'[A-Za-z]', password1):
            self.add_error(
                'password1', const.PASSWORD_MUST_CONTAIN_LETTERS_ERROR
            )

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
