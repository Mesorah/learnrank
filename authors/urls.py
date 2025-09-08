from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from authors import views

app_name = 'authors'

urlpatterns = [
    path('login/', views.LoginAuthorView.as_view(), name='login'),
    path('signup/', views.CreateAuthorView.as_view(), name='signup'),
    path('logout/', views.logout_author, name='logout'),
    path('delete/', views.DeleteAuthorView.as_view(), name='delete'),

    path(
        'change-username/',
        views.ChangeUsernameView.as_view(),
        name='change_username'
    ),

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

    path(
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'api/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),
]
