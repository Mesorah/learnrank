from django.urls import path

from authors import views

app_name = 'authors'

urlpatterns = [
    path('signup/', views.create_author, name='signup'),
]
