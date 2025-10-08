from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic.base import View

import authors.constants as const
from authors.forms import ChangeUsernameForm

HOME_PAGE = 'home:index'
LOGIN_PAGE = 'authors:login'
AUTHORS_TEMPLATE = 'authors/pages/authors.html'


class ChangeUsernameView(View):
    """

    The LoginErrorMixin cannot be used here due to the POST request.

    """

    def render_form(self, form):
        return render(self.request, AUTHORS_TEMPLATE, context={
            'form_action': 'authors:change_username',
            'title': const.TITLE_CHANGE_USERNAME,
            'form': form
        })

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, const.CANNOT_ACCESS_NOT_LOGGED_ERROR)

            return redirect(LOGIN_PAGE)

        return super().dispatch(request, *args, **kwargs)

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
