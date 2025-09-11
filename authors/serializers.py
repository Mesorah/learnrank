from rest_framework import serializers


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(min_length=4, max_length=30)
    email = serializers.EmailField(max_length=256)
    change_username_data = serializers.DateTimeField(
        read_only=True,
        allow_null=True
    )
