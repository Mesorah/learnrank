from django.urls import path

from authors import views

app_name = 'authors'

urlpatterns = [
    path('login/', views.LoginAuthorView.as_view(), name='login'),
    path('signup/', views.CreateAuthorView.as_view(), name='signup'),
    path('logout/', views.logout_author, name='logout'),
]
