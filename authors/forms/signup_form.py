from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

import authors.constants as const
from authors.validators import AuthorValidator

User = get_user_model()


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
            'unique': const.USERNAME_ALREADY_TAKEN_ERROR
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
        max_length=50, widget=forms.PasswordInput(
            attrs={'placeholder': const.SIGNUP_PASSWORD1_PLACEHOLDER}
        )
    )
    password2 = forms.CharField(
        label=const.PASSWORD2_LABEL,
        min_length=8,
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
            validation_error=ValidationError,
            add_error=self.add_error,
            context='form'
        )

        return super_clean

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
