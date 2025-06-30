from django.shortcuts import render

from authors.forms import CustomSignupForm


def create_author(request):
    form = CustomSignupForm()

    return render(request, 'authors/pages/authors.html', context={
        'form': form
    })
