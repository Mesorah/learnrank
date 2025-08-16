from django.contrib.auth import get_user_model

User = get_user_model()


def login(client, username='testing', password='testing12!@1dsFG'):
    client.login(username=username, password=password)


def create_user(
    username='testing',
    email='testing@example.com',
    password='testing12!@1dsFG',
    auto_login=False,
    client=None
):

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    if auto_login and client:
        login(client)

    return user
