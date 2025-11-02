from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import translation

import authors.constants as const


class LoginErrorMixin:
    """
    Note that with authenticated_user = False, it validates whether the
    user is not logged in, and with authenticated_user = True, it validates
    whether the user is logged in. If authenticated_user = False and the
    user is logged in, it throws an error, and the same applies if
    authenticated_user = True and the user is logged out.
    """

    authenticated_user = False
    message = const.CANNOT_ACCESS_LOGGED_ERROR
    redirect_page = const.HOME_PAGE

    def dispatch(self, request, *args, **kwargs):
        is_authenticated = request.user.is_authenticated

        if not self.authenticated_user and not is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        if self.authenticated_user and is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        messages.error(request, self.message)

        return redirect(reverse(self.redirect_page))


class AuthViewMixin:
    title = None
    form_action = None
    title_key = None
    is_signup = False

    success_message = None
    error_message = const.FORM_INVALID_ERROR

    def get_success_url(self):
        return self.success_url

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['title'] = self.title
        ctx['html_language'] = translation.get_language()
        ctx['form_action'] = self.form_action
        ctx['title_key'] = self.title_key
        ctx['is_signup'] = self.is_signup

        return ctx


class RenderFormMixin:
    template = const.AUTHORS_TEMPLATE
    form_action = None
    title = None
    form = None

    def render_form(self, form):
        return render(self.request, self.template, context={
            'form_action': self.form_action,
            'title': self.title,
            'form': form
        })
