from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext as _

from authors.forms import CustomSignupForm


def create_author(request):
    if request.user.is_authenticated:
        messages.error(request, _('You cannot access this while logged in.'))

        return redirect(reverse('home:index'))

    if request.method == 'POST':
        form = CustomSignupForm(request.POST)

        if form.is_valid():
            messages.success(request, _('Account created!'))
            user = form.save()

            login(request, user)

            return redirect(reverse('home:index'))

        else:
            messages.error(request, _('Form inválid.'))

    else:
        form = CustomSignupForm()

    html_language = translation.get_language()
    signup_translation = _('Sign Up')

    return render(request, 'authors/pages/authors.html', context={
        'form': form,
        'title': signup_translation,
        'html_language': html_language
    })
