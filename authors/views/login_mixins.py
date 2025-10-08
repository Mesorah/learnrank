from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

import authors.constants as const


class LoginErrorMixin:
    message = const.CANNOT_ACCESS_LOGGED_ERROR
    authenticated_user = False

    def dispatch(self, request, *args, **kwargs):
        is_authenticated = request.user.is_authenticated

        if not self.authenticated_user and not is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        if self.authenticated_user and is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        messages.error(request, self.message)

        return redirect(reverse(const.HOME_PAGE))
