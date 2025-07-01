from django.shortcuts import render

from authors.forms import CustomSignupForm


def create_author(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data.get('password1'))
            print(form.cleaned_data.get('password2'))
            form.save()

    else:
        form = CustomSignupForm()

    return render(request, 'authors/pages/authors.html', context={
        'form': form
    })
