from django.contrib.auth import get_user_model
from rest_framework import serializers

import authors.constants as const
from authors.validators import AuthorValidator

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'id', 'username', 'email', 'change_username_data',
            'password'
        ]

    username = serializers.CharField(
        max_length=30,
        error_messages={
            'min_length': const.USERNAME_MIN_LENGTH_ERROR,
        },
    )

    email = serializers.EmailField(
        max_length=256, required=True
    )

    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)

        AuthorValidator(
            values=attrs,
            ValidationError=serializers.ValidationError,
            context='serializer'
        )

        return attrs
