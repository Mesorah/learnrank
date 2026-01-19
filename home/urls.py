from django.urls import path

from home import views

app_name = 'home'


urlpatterns = [
    path('', views.index, name='index'),
    path('classes/', views.classes, name='classes'),
]
