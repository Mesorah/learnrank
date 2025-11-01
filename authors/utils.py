from django.utils import timezone


def is_wait_time_done(wait_days=7):
    """
    Take today's date and subtract it from wait_days

    Ex:
        time_now = 1/11/2025
        time_delta = 7

        new_data = time_now - time_delta -> 25/10/2025
    """

    time_now = timezone.now()
    time_delta = timezone.timedelta(days=wait_days)

    new_date = time_now - time_delta

    return new_date


def change_username(user, cleaned_data):
    user.username = cleaned_data.get('new_username', user.username)

    user.change_username_data = timezone.now()

    user.save()

    return user
