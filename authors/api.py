from django.contrib.auth import get_user_model
from rest_framework.generics import (  # noqa E501
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated

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


class AuthorAPIDetail(RetrieveUpdateDestroyAPIView):
    http_method_names = ['get', 'patch', 'delete', 'options', 'head']
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = AuthorSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'PATCH']:
            return [IsAdminOrSelf()]

        return [IsAdminUser()]
