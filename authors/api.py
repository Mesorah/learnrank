from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from authors.serializers import AuthorSerializer

User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAdminUser])
def author_api_list(request):
    users = User.objects.all()
    serializer = AuthorSerializer(users, many=True)

    return Response(serializer.data)
