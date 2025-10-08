from django.contrib import messages
from django.contrib.auth.views import (
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import reverse_lazy

import authors.constants as const
from authors.forms import CustomPasswordResetForm, CustomSetPasswordForm


class PasswordResetAuthorView(PasswordResetView):
    success_url = reverse_lazy('authors:password_reset_done')
    template_name = 'authors/pages/password_reset.html'
    email_template_name = 'authors/pages/password_reset_email.html'
    form_class = CustomPasswordResetForm


class PasswordResetDoneAuthorView(PasswordResetDoneView):
    template_name = 'authors/pages/password_reset_done.html'


class PasswordResetConfirmAuthorView(PasswordResetConfirmView):
    success_url = reverse_lazy(const.HOME_PAGE)
    template_name = 'authors/pages/password_reset.html'
    form_class = CustomSetPasswordForm

    def form_valid(self, form):
        messages.success(self.request, const.PASSWORD_CHANGED_SUCCESS)
        return super().form_valid(form)
