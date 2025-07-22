from django.urls import path

from authors import views

app_name = 'authors'

urlpatterns = [
    path('login/', views.LoginAuthorView.as_view(), name='login'),
    path('signup/', views.CreateAuthorView.as_view(), name='signup'),
    path('logout/', views.logout_author, name='logout'),
    path('delete/', views.delete_author, name='delete'),

    path(
        'password-reset/',
        views.PasswordResetAuthorView.as_view(),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        views.PasswordResetDoneAuthorView.as_view(),
        name='password_reset_done'
    ),
    path(
        'password-reset/confirm/<uidb64>/<token>/',
        views.PasswordResetConfirmAuthorView.as_view(),
        name='password_reset_confirm'
    ),
]
