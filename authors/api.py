from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authors.permissions import IsAdminOrSelf
from authors.serializers import AuthorSerializer

User = get_user_model()


class AuthorAPIPagination(PageNumberPagination):
    page_size = 5


class AuthorAPIList(ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = AuthorSerializer
    pagination_class = AuthorAPIPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]

        return [IsAdminUser()]


class AuthorAPIDetail(APIView):
    def get_permissions(self):
        if self.request.method in ['GET', 'PATCH']:
            return [IsAdminOrSelf()]

        return [IsAdminUser()]

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        serializer = AuthorSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        user.delete()

        return Response(status=status.HTTP_200_OK)
