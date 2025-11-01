from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

import authors.constants as const


class LoginErrorMixin:
    """
    Note that with authenticated_user = False, it validates whether the
    user is not logged in, and with authenticated_user = True, it validates
    whether the user is logged in. If authenticated_user = False and the
    user is logged in, it throws an error, and the same applies if
    authenticated_user = True and the user is logged out.
    """

    authenticated_user = False
    message = const.CANNOT_ACCESS_LOGGED_ERROR
    redirect_page = const.HOME_PAGE

    def dispatch(self, request, *args, **kwargs):
        is_authenticated = request.user.is_authenticated

        if not self.authenticated_user and not is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        if self.authenticated_user and is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        messages.error(request, self.message)

        return redirect(reverse(self.redirect_page))
