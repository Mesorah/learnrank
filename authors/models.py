from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    change_username_data = models.DateTimeField(
        null=True, blank=True, default=None
    )
