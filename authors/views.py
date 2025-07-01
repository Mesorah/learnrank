from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.forms import CustomSignupForm


def create_author(request):
    if request.user.is_authenticated:
        messages.error(request, 'you cannot access this while logged in.')

        return redirect(reverse('home:index'))

    if request.method == 'POST':
        form = CustomSignupForm(request.POST)

        if form.is_valid():
            messages.success(request, 'Account created!')
            user = form.save()

            login(request, user)

            return redirect(reverse('home:index'))

        else:
            messages.error(request, 'Form inválid.')

    else:
        form = CustomSignupForm()

    return render(request, 'authors/pages/authors.html', context={
        'form': form,
        'title': 'Sign Up'
    })
