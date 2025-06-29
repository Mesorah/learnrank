from django.shortcuts import render


def create_author(request):
    return render(request, 'authors/pages/authors.html')
