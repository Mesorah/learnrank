from django.shortcuts import render

TITLE_HOME = 'Home'


def index(request):
    return render(request, 'home/pages/index.html', context={
        'title': TITLE_HOME
    })
