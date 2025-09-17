from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authors.permissions import IsAdminOrSelf
from authors.serializers import AuthorSerializer

User = get_user_model()


class AuthorAPIList(APIView):
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'patch']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]

        return [IsAdminUser()]

    def get(self, request):
        users = User.objects.all()
        serializer = AuthorSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AuthorAPIDetail(APIView):
    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsAdminOrSelf()]

        return [IsAdminUser()]

    def patch(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        serializer = AuthorSerializer(
            user, data=request.data, partial=True,
            context={'request': request, 'view': self}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
