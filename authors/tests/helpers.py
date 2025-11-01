from django.contrib.auth import get_user_model

import utils.constants_informations as const_informations
from authors.utils import is_wait_time_done

User = get_user_model()


def login(client, **kwargs):
    username = kwargs.get('username', const_informations.TEST_USERNAME)
    password = kwargs.get('password', const_informations.TEST_PASSWORD)

    client.login(username=username, password=password)


def create_user(auto_login=False, client=None, qtd=1, **kwargs):
    username = kwargs.get('username', const_informations.TEST_USERNAME)
    email = kwargs.get('email', const_informations.TEST_EMAIL)
    password = kwargs.get('password', const_informations.TEST_PASSWORD)

    for user_number in range(qtd):
        final_username = f'{username}-{user_number}' if qtd > 1 else username
        final_email = f'{username}-{user_number}' if qtd > 1 else email

        user = User.objects.create_user(
            username=final_username,
            email=final_email,
            password=password
        )

    if auto_login and client:
        login(client)

    return user


def create_admin_user(
    auto_login=False,
    client=None,
    **kwargs
):
    username = kwargs.get('username', const_informations.TEST_USERNAME_ADMIN)
    email = kwargs.get('email', const_informations.TEST_EMAIL_ADMIN)
    password = kwargs.get('password', const_informations.TEST_PASSWORD_ADMIN)

    super_user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )

    if auto_login and client:
        client.force_login(super_user)

    return super_user


def change_username_data(user, wait_days=7):
    # get how many days left to change username
    new_data = is_wait_time_done(wait_days=wait_days)

    user.change_username_data = new_data
    user.save()

    return user.change_username_data
