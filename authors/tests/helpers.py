from django.contrib.auth import get_user_model

from authors.utils import is_wait_time_done

User = get_user_model()


def login(client, username='testing', password='testing12!@1dsFG'):
    client.login(username=username, password=password)


def create_user(
    username='testing',
    email='testing@example.com',
    password='testing12!@1dsFG',
    auto_login=False,
    client=None,
    qtd=1
):
    for user in range(qtd):
        final_username = f'{username}-{user}' if qtd != 1 else username
        final_email = f'{username}-{user}' if qtd != 1 else email

        user = User.objects.create_user(
            username=final_username,
            email=final_email,
            password=password
        )

    if auto_login and client:
        login(client)

    return user


def create_admin_user(
    username='testingADMIN',
    email='testingADMIN@example.com',
    password='testing12ADMIN!@1dsFG',
    auto_login=False,
    client=None,
):
    super_user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )

    if auto_login and client:
        client.force_login(super_user)

    return super_user


def change_username_data(user, wait_days=7):
    new_data = is_wait_time_done(wait_days=wait_days)

    user.change_username_data = new_data
    user.save()

    return user.change_username_data
