from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils import translation
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.views.generic import CreateView

from authors.forms import CustomSignupForm

User = get_user_model()


class CreateAuthorView(CreateView):
    model = User
    form_class = CustomSignupForm
    template_name = 'authors/pages/authors.html'
    success_url = reverse_lazy('home:index')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, _(
                'You cannot access this while logged in.'
            ))

            return redirect(reverse('home:index'))

        return super().dispatch(request, *args, **kwargs)

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

        return ctx


@require_POST
@login_required(login_url=reverse_lazy('authors:signup'))
def logout_author(request):
    logout(request)
    messages.success(request, _('Success, you have logged out!'))

    return redirect('authors:signup')


def login_author(request):
    pass
