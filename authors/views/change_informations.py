from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic.base import View

import authors.constants as const
from authors.forms import ChangeUsernameForm

from .login_mixins import LoginErrorMixin

HOME_PAGE = 'home:index'
LOGIN_PAGE = 'authors:login'
AUTHORS_TEMPLATE = 'authors/pages/authors.html'


class ChangeUsernameView(LoginErrorMixin, View):
    message = const.CANNOT_ACCESS_NOT_LOGGED_ERROR
    authenticated_user = True
    redirect_page = LOGIN_PAGE

    def render_form(self, form):
        return render(self.request, AUTHORS_TEMPLATE, context={
            'form_action': 'authors:change_username',
            'title': const.TITLE_CHANGE_USERNAME,
            'form': form
        })

    def get(self, *args, **kwargs):
        form = ChangeUsernameForm(self.request.user)

        return self.render_form(form)

    def post(self, *args, **kwargs):
        form = ChangeUsernameForm(self.request.user, self.request.POST)

        if form.is_valid():
            form.save()

            messages.success(self.request, const.USERNAMED_CHANGED_SUCCESS)

            return redirect(HOME_PAGE)

        return self.render_form(form)


def change_email(request):
    # TODO
    pass
