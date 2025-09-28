from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import empty

import authors.constants as const
from authors.utils import change_username
from authors.validators import (
    AuthorPATCHValidator,
    AuthorValidator,
    CheckAuthorUsernameValidator,
)

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

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)

        self.request = self.context.get('request')

        if self.request and self.request.method == 'PATCH':
            self.actual_username = instance.username
            self.change_username_data = instance.change_username_data
            self.new_username = data.get('username')
            self.is_staff = self.request.user.is_staff

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if self.request and self.request.method == 'PATCH':
            AuthorPATCHValidator(
                values=attrs,
                change_username_data=self.change_username_data,
                ValidationError=serializers.ValidationError,
                is_staff=self.is_staff
            )

        else:
            AuthorValidator(
                values=attrs,
                ValidationError=serializers.ValidationError,
                context='serializer',
            )

        return attrs

    def save(self, **kwargs):
        super_save = super().save(**kwargs)

        if self.request and self.request.method == 'PATCH':
            return change_username(
                user=self.request.user,
                cleaned_data=self.validated_data
            )

        return super_save


class CheckAuthorUsernameSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=4, max_length=30)

    def validate(self, attrs):
        attrs = super().validate(attrs)

        CheckAuthorUsernameValidator(
            values=attrs,
            ValidationError=serializers.ValidationError,
        )

        return attrs
