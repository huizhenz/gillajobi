from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    UserDetailSerializer,
    ProfileSerializer,
)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def profile(request):

    if request.method == 'GET':

        user_serializer = UserDetailSerializer(
            request.user
        )

        profile_serializer = ProfileSerializer(
            request.user.profile
        )

        return Response({
            'user': user_serializer.data,
            'profile': profile_serializer.data,
        })

    elif request.method == 'PATCH':

        serializer = ProfileSerializer(
            request.user.profile,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)