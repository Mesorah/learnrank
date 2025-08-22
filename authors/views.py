from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import translation
from django.views.decorators.http import require_POST
from django.views.generic import CreateView
from django.views.generic.base import View

import authors.constants as const
from authors.forms import (
    ChangeInformationForm,
    ConfirmForm,
    CustomAuthenticationForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    CustomSignupForm,
)

User = get_user_model()


class LoginErrorMixin:
    message = const.CANNOT_ACCESS_LOGGED_ERROR
    authenticated_user = False

    def dispatch(self, request, *args, **kwargs):
        is_authenticated = request.user.is_authenticated

        if not self.authenticated_user and not is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        if self.authenticated_user and is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        messages.error(request, self.message)

        return redirect(reverse('home:index'))


class CreateAuthorView(LoginErrorMixin, CreateView):
    model = User
    form_class = CustomSignupForm
    template_name = 'authors/pages/authors.html'
    success_url = reverse_lazy('home:index')

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


@require_POST
@login_required(login_url=reverse_lazy('authors:login'))
def logout_author(request):
    logout(request)
    messages.success(request, const.ACCOUNT_LOGOUT_SUCCESS)

    return redirect('authors:login')


class LoginAuthorView(LoginErrorMixin, LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'authors/pages/authors.html'
    success_url = reverse_lazy('home:index')

    def get_success_url(self):
        return self.success_url

    def form_valid(self, form):
        messages.success(self.request, const.ACCOUNT_LOGGED_SUCCESS)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['title'] = const.TITLE_LOGIN
        ctx['html_language'] = translation.get_language()
        ctx['form_action'] = 'authors:login'
        ctx['title_key'] = 'Login'

        return ctx


class DeleteAuthorView(LoginErrorMixin, View):
    message = const.CANNOT_ACCESS_NOT_LOGGED_ERROR
    authenticated_user = True

    def render_form(self, form):
        return render(self.request, 'authors/pages/authors.html', context={
            'form_action': 'authors:delete',
            'form': form,
            'title': const.TITLE_DELETE_ACCOUNT,
        })

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

            return redirect('home:index')

        return self.render_form(form)


@login_required(login_url=reverse_lazy('authors:login'))
def change_information(request):
    form = ChangeInformationForm(request.user)

    if request.method == 'POST':
        form = ChangeInformationForm(request.user, request.POST)

        if form.is_valid():
            form.save()

            return redirect('home:index')

    return render(request, 'authors/pages/authors.html', context={
        'form_action': 'authors:change_information',
        'title': 'Change username',  # TODO change the title
        'form': form
    })


class PasswordResetAuthorView(PasswordResetView):
    success_url = reverse_lazy('authors:password_reset_done')
    template_name = 'authors/pages/password_reset.html'
    email_template_name = 'authors/pages/password_reset_email.html'
    form_class = CustomPasswordResetForm


class PasswordResetDoneAuthorView(PasswordResetDoneView):
    template_name = 'authors/pages/password_reset_done.html'


class PasswordResetConfirmAuthorView(PasswordResetConfirmView):
    success_url = reverse_lazy('home:index')
    template_name = 'authors/pages/password_reset.html'
    form_class = CustomSetPasswordForm

    def form_valid(self, form):
        messages.success(self.request, const.PASSWORD_CHANGED_SUCCESS)
        return super().form_valid(form)
