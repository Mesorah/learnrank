from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.base import View

import authors.constants as const
from authors.forms import ConfirmForm

from .mixins import LoginErrorMixin, RenderFormMixin


class DeleteAuthorView(LoginErrorMixin, RenderFormMixin, View):
    message = const.CANNOT_ACCESS_NOT_LOGGED_ERROR
    authenticated_user = True

    template = const.AUTHORS_TEMPLATE
    form_action = const.DELETE_PAGE
    title = const.TITLE_DELETE_ACCOUNT

    def get(self, *args, **kwargs):
        form = ConfirmForm()
        return self.render_form(form)

    def post(self, *args, **kwargs):
        form = ConfirmForm(self.request.POST)

        if form.is_valid():
            user = self.request.user
            user.delete()

            messages.success(
                self.request, const.ACCOUNT_DELETED_SUCCESS
            )

            return redirect(const.HOME_PAGE)

        return self.render_form(form)
