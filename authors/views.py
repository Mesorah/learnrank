from django.contrib import messages
from django.shortcuts import render

from authors.forms import CustomSignupForm


def create_author(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)

        if form.is_valid():
            messages.success(request, 'Account created!')
            form.save()
        else:
            messages.error(request, 'Form inválid.')

    else:
        form = CustomSignupForm()

    return render(request, 'authors/pages/authors.html', context={
        'form': form
    })
