from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy

import authors.constants as authors_const
import courses.constants as const


@login_required(login_url=reverse_lazy(authors_const.LOGIN_PAGE))
def index(request):
    return render(request, 'courses/pages/index.html', context={
        'title': const.TITLE_INDEX
    })
