from django import forms
from django.core.exceptions import ValidationError

import authors.constants as const


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
