from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import translation
from django.views.decorators.http import require_POST
from django.views.generic import CreateView

import authors.constants as const
from authors.forms import CustomAuthenticationForm, CustomSignupForm

from .login_mixins import LoginErrorMixin

User = get_user_model()


class CreateAuthorView(LoginErrorMixin, CreateView):
    model = User
    form_class = CustomSignupForm
    template_name = const.AUTHORS_TEMPLATE
    success_url = reverse_lazy(const.HOME_PAGE)

    def get_success_url(self):
        return self.success_url

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)

        messages.success(self.request, const.ACCOUNT_CREATED_SUCCESS)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, const.FORM_INVALID_ERROR)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['title'] = const.TITLE_SIGN_UP
        ctx['html_language'] = translation.get_language()
        ctx['form_action'] = 'authors:signup'
        ctx['is_signup'] = True
        ctx['title_key'] = 'Sign Up'

        return ctx


class LoginAuthorView(LoginErrorMixin, LoginView):
    form_class = CustomAuthenticationForm
    template_name = const.AUTHORS_TEMPLATE
    success_url = reverse_lazy(const.HOME_PAGE)

    def get_success_url(self):
        return self.success_url

    def form_valid(self, form):
        messages.success(self.request, const.ACCOUNT_LOGGED_SUCCESS)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['title'] = const.TITLE_LOGIN
        ctx['html_language'] = translation.get_language()
        ctx['form_action'] = const.LOGIN_PAGE
        ctx['title_key'] = 'Login'

        return ctx


@require_POST
@login_required(login_url=reverse_lazy(const.LOGIN_PAGE))
def logout_author(request):
    logout(request)
    messages.success(request, const.ACCOUNT_LOGOUT_SUCCESS)

    return redirect(const.LOGIN_PAGE)
