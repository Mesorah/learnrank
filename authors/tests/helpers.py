from django.contrib.auth import get_user_model

User = get_user_model()


def login(client, username='testing', password='testing12!@1dsFG'):
    client.login(username=username, password=password)


def create_user(
    username='testing',
    email='testing@example.com',
    password='testing12!@1dsFG',
    auto_login=False,
    client=None,
    users=1
):
    for user in range(users):
        final_username = f'{username}-{user}' if users != 1 else username
        final_email = f'{username}-{user}' if users != 1 else email

        user = User.objects.create_user(
            username=final_username,
            email=final_email,
            password=password
        )

    if auto_login and client:
        login(client)

    return user


def create_admin_user(
    username='testing',
    email='testing@example.com',
    password='testing12!@1dsFG',
):
    super_user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )

    return super_user
