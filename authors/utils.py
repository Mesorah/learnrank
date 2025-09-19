from django.utils import timezone


def is_wait_time_done(wait_days=7):
    time_now = timezone.now()
    time_delta = timezone.timedelta(days=wait_days)

    new_date = time_now - time_delta

    return new_date


def change_username(user, cleaned_data):
    user.username = cleaned_data.get(
            'new_username', user.username
    )

    user.change_username_data = timezone.now()

    user.save()

    return user
