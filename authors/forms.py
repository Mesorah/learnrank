import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

User = get_user_model()


class CustomSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'email',
            'password1', 'password2'
        ]

    username = forms.CharField(
        max_length=30, min_length=4, widget=forms.TextInput(
            attrs={'placeholder': 'Ex: Gabriel Rodrigues'}
        )
    )
    email = forms.EmailField(
        max_length=256, widget=forms.EmailInput(
            attrs={'placeholder': 'Ex: gabrielrodrigues@example.com'}
        )
    )
    password1 = forms.CharField(
        max_length=50, min_length=4, widget=forms.PasswordInput(
            attrs={'placeholder': 'Ex 23#$1fsgKDL!'}
        )
    )
    password2 = forms.CharField(
        max_length=50, min_length=4, widget=forms.PasswordInput(
            attrs={'placeholder': 'Repeat your password'}
        )
    )

    def clean_username(self):
        username = self.cleaned_data['username']

        if len(username) < 4:
            raise ValidationError('Size less than 4 characters.')

        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already in use.')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already in use.')

        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError('Passwords are not the same.')

        if len(password1) < 8 or len(password2) < 8:
            raise ValidationError('Size smaller than 8 characters.')

        # Verify if password1 have [a-z] or [1-9] and don't have symbols
        if password1.isalnum():
            raise ValidationError('Without the use of symbols.')

        # Verify if password1 don't have numbers [1-9]
        if not re.search(r'\d', password1):
            raise ValidationError('Without the use of numbers.')

        if not re.search(r'[A-Za-z]', password1):
            raise ValidationError('Without the use of characters.')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
