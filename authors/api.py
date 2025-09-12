from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from authors.serializers import AuthorSerializer

User = get_user_model()


class AuthorAPIList(APIView):
    permission_classes = [IsAdminUser]
    http_method_names = ['get']

    def get(self, request):
        users = User.objects.all()
        serializer = AuthorSerializer(users, many=True)

        return Response(serializer.data)
