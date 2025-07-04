import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CustomSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'email',
            'password1', 'password2'
        ]

    username = forms.CharField(
        label=_('Username'),
        min_length=4,
        error_messages={'min_length': _(
            'Please enter at least 4 characters.'
        )},
        max_length=30, widget=forms.TextInput(
            attrs={'placeholder': 'Ex: Gabriel Rodrigues'}
        ),
    )
    email = forms.EmailField(
        label=_('Email'),
        max_length=256, widget=forms.EmailInput(
            attrs={'placeholder': 'Ex: gabrielrodrigues@example.com'}
        )
    )
    password1 = forms.CharField(
        label=_('Password'),
        min_length=8,
        error_messages={'min_length': _(
            'Please enter at least 8 characters.'
        )},
        max_length=50, widget=forms.PasswordInput(
            attrs={'placeholder': 'Ex 23#$1fsgKDL!'}
        )
    )
    password2 = forms.CharField(
        label=_('Repeat password'),
        min_length=8,
        error_messages={'min_length': _(
            'Please enter at least 8 characters.'
        )},
        max_length=50, widget=forms.PasswordInput(
            attrs={'placeholder': _('Repeat your password')}
        )
    )

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise ValidationError(_('Username is already taken.'))

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise ValidationError(_('Email is already registered.'))

        return email

    def clean(self):
        cleaned_data = self.cleaned_data
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            self.add_error('password2', _('Passwords do not match.'))

        # Verify if password1 have [a-z] or [1-9] and don't have symbols
        if password1 and password1.isalnum():
            self.add_error('password1', _(
                'The password must contain symbols.'
            ))

        # Verify if password1 don't have numbers [1-9]
        if not re.search(r'\d', password1):
            self.add_error('password1', _(
                'Password must contain numbers.'
            ))

        if not re.search(r'[A-Za-z]', password1):
            self.add_error('password1', _(
                'Password must contain letters.'
            ))

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
