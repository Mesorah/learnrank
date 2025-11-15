from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView

import authors.constants as const
from authors.forms import CustomAuthenticationForm, CustomSignupForm

from .mixins import AuthViewMixin, LoginErrorMixin

User = get_user_model()


class CreateAuthorView(LoginErrorMixin, AuthViewMixin, CreateView):
    model = User
    form_class = CustomSignupForm
    template_name = const.AUTHORS_TEMPLATE
    success_url = reverse_lazy(const.HOME_PAGE)

    title = const.TITLE_SIGN_UP
    form_action = const.SIGNUP_PAGE
    title_key = const.SIGNUP_TITLE_KEY
    is_signup = True

    success_message = const.ACCOUNT_CREATED_SUCCESS
    error_message = const.FORM_INVALID_ERROR

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)

        messages.success(self.request, const.ACCOUNT_CREATED_SUCCESS)
        return redirect(self.get_success_url())


class LoginAuthorView(LoginErrorMixin, AuthViewMixin, LoginView):
    form_class = CustomAuthenticationForm
    template_name = const.AUTHORS_TEMPLATE
    success_url = reverse_lazy(const.HOME_PAGE)

    title = const.TITLE_LOGIN
    form_action = const.LOGIN_PAGE
    title_key = const.LOGIN_TITLE_KEY

    success_message = const.ACCOUNT_LOGGED_SUCCESS
    error_message = const.FORM_INVALID_ERROR


@require_POST
@login_required(login_url=reverse_lazy(const.LOGIN_PAGE))
def logout_author(request):
    logout(request)
    messages.success(request, const.ACCOUNT_LOGOUT_SUCCESS)

    return redirect(const.LOGIN_PAGE)
