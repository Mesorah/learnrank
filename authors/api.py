from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.generics import (  # noqa E501
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from authors.permissions import IsAdminOrSelf
from authors.serializers import AuthorSerializer, CheckAuthorUsernameSerializer

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


@csrf_exempt
@api_view(http_method_names=['POST'])
def author_api_check_username(request):
    serializer = CheckAuthorUsernameSerializer(data=request.data)
    username = request.data.get('username')

    can_use = not User.objects.filter(username=username).exists()
    username_is_valid = serializer.is_valid()

    return Response({'success': username_is_valid and can_use})
