import json
import threading

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
from ai_score.services import compute_scores_for_user, invalidate_user_scores, _is_profile_empty


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def profile(request):

    if request.method == 'GET':

        user_serializer = UserDetailSerializer(
            request.user, context={'request': request})
        profile_serializer = ProfileSerializer(request.user.profile)

        return Response({
            'user': user_serializer.data,
            'profile': profile_serializer.data,
        })

    elif request.method == 'PATCH':

        user_data = {}
        for field in ['first_name', 'last_name']:
            if field in request.data:
                user_data[field] = request.data[field]
        if 'profile_image' in request.FILES:
            user_data['profile_image'] = request.FILES['profile_image']

        if user_data:
            user_serializer = UserDetailSerializer(
                request.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        # Profile 필드 - JSON 문자열이므로 파싱 필요
        profile_data = {}
        array_fields = ['education', 'certification', 'experience',
                        'language', 'preferred_location', 'preferred_position']
        for field in array_fields:
            if field in request.data:
                value = request.data[field]
                try:
                    profile_data[field] = json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    profile_data[field] = value
        if 'desired_salary' in request.data:
            profile_data['desired_salary'] = request.data['desired_salary']

        profile_serializer = ProfileSerializer(
            request.user.profile, data=profile_data, partial=True)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()

        # 기존 점수 삭제 후 백그라운드에서 재계산
        invalidate_user_scores(request.user)
        if not _is_profile_empty(request.user.profile):
            t = threading.Thread(
                target=compute_scores_for_user,
                args=(request.user,),
                daemon=True,
            )
            t.start()

        return Response({
            'user': UserDetailSerializer(request.user, context={'request': request}).data,
            'profile': profile_serializer.data,
        })
