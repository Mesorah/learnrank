from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.base import View

import authors.constants as const
from authors.forms import ChangeUsernameForm

from .mixins import LoginErrorMixin, RenderFormMixin


class ChangeUsernameView(LoginErrorMixin, RenderFormMixin, View):
    message = const.CANNOT_ACCESS_NOT_LOGGED_ERROR
    authenticated_user = True
    redirect_page = const.LOGIN_PAGE

    template = const.AUTHORS_TEMPLATE
    form_action = const.CHANGE_USERNAME_PAGE
    title = const.TITLE_CHANGE_USERNAME

    def get(self, *args, **kwargs):
        form = ChangeUsernameForm(self.request.user)

        return self.render_form(form)

    def post(self, *args, **kwargs):
        form = ChangeUsernameForm(self.request.user, self.request.POST)

        if form.is_valid():
            form.save()

            messages.success(self.request, const.USERNAMED_CHANGED_SUCCESS)

            return redirect(const.HOME_PAGE)

        return self.render_form(form)


def change_email(request):
    # TODO
    pass
