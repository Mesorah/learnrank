from django.http import HttpResponse
from django.urls import path

app_name = 'home'


def index(request):
    return HttpResponse('.')


urlpatterns = [
    path('index/', index, name='index'),
]
