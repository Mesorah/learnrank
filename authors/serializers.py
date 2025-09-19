from django.contrib.auth import get_user_model
from rest_framework import serializers

import authors.constants as const
from authors.utils import change_username
from authors.validators import AuthorValidator, ChangeUsernameValidator

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

    def __init__(self, instance=None, data=None, **kwargs):
        super().__init__(instance, data, **kwargs)

        self.request = self.context.get('request')

        if self.request and self.request.method == 'PATCH':
            self.actual_username = instance.username
            self.change_username_data = instance.change_username_data
            self.new_username = data['username']
            self.is_staff = self.request.user.is_staff

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if self.request and self.request.method == 'PATCH':
            ChangeUsernameValidator(
                change_username_data=self.change_username_data,
                new_username=self.new_username,
                ValidationError=serializers.ValidationError,
                is_staff=self.is_staff
            )

        else:
            AuthorValidator(
                values=attrs,
                ValidationError=serializers.ValidationError,
                context='serializer',
                method=self.request.method if self.request else None
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
