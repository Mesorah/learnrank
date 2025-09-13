from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'id', 'username', 'email', 'change_username_data'
        ]
