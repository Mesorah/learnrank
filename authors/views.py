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
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView
from django.views.generic.base import View

from authors.forms import (
    ConfirmForm,
    CustomAuthenticationForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    CustomSignupForm,
)

User = get_user_model()


class LoginErrorMixin(View):
    message = _lazy('You cannot access this while logged in.')
    authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        is_authenticated = request.user.is_authenticated

        if not self.authenticated_user and is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        if self.authenticated_user and not is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        messages.error(request, self.message)

        return redirect(reverse('home:index'))


class CreateAuthorView(CreateView, LoginErrorMixin):
    model = User
    form_class = CustomSignupForm
    template_name = 'authors/pages/authors.html'
    success_url = reverse_lazy('home:index')

    def get_success_url(self):
        return self.success_url

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)

        messages.success(self.request, _('Account created!'))
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, _('Form invalid.'))
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['title'] = _('Sign Up')
        ctx['html_language'] = translation.get_language()
        ctx['form_action'] = 'authors:signup'
        ctx['is_signup'] = True
        ctx['title_key'] = 'Sign Up'

        return ctx


@require_POST
@login_required(login_url=reverse_lazy('authors:login'))
def logout_author(request):
    logout(request)
    messages.success(request, _('Success, you have logged out!'))

    return redirect('authors:login')


class LoginAuthorView(LoginView, LoginErrorMixin):
    form_class = CustomAuthenticationForm
    template_name = 'authors/pages/authors.html'
    success_url = reverse_lazy('home:index')

    def get_success_url(self):
        return self.success_url

    def form_valid(self, form):
        messages.success(self.request, _('Account logged!'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['title'] = _('Login')
        ctx['html_language'] = translation.get_language()
        ctx['form_action'] = 'authors:login'
        ctx['title_key'] = 'Login'

        return ctx


def delete_author(request):
    form = ConfirmForm()

    if not request.user.is_authenticated:
        messages.error(
            request,
            _('You cannot access this while not logged in.')
        )

        return redirect('home:index')

    if request.method == 'POST':
        form = ConfirmForm(request.POST)

        if form.is_valid():
            user = request.user
            user.delete()

            messages.success(
                request, _('Your account has been successfully deleted!')
            )

            return redirect('home:index')

    return render(request, 'authors/pages/authors.html', context={
        'form_action': 'authors:delete',
        'form': form,
        'title': _('Delete your account'),
    })


class PasswordResetAuthorView(PasswordResetView):
    success_url = reverse_lazy('authors:password_reset_done')
    template_name = 'authors/pages/password_reset.html'
    email_template_name = 'authors/pages/password_reset_email.html'
    # message = _lazy('You cannot access this while not logged in.')
    # authenticated_user = False
    form_class = CustomPasswordResetForm


class PasswordResetDoneAuthorView(PasswordResetDoneView):
    template_name = 'authors/pages/password_reset_done.html'


class PasswordResetConfirmAuthorView(PasswordResetConfirmView):
    success_url = reverse_lazy('home:index')
    template_name = 'authors/pages/password_reset.html'
    form_class = CustomSetPasswordForm

    def form_valid(self, form):
        messages.success(self.request, _('Password changed successfully!'))
        return super().form_valid(form)
