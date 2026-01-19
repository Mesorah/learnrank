from django.shortcuts import render

import courses.constants as const


def index(request):
    return render(request, 'courses/pages/index.html', context={
        'title': const.TITLE_INDEX
    })
