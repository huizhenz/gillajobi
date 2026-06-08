from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Profile
from .serializers import UserSerializer, ProfileSerializer


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_profile(request):
    serializer = ProfileSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def profile(request):
    user_serializer = UserSerializer(request.user)

    profile = Profile.objects.get(user=request.user)
    profile_serializer = ProfileSerializer(profile)

    return Response({
        'user': user_serializer.data,
        'profile': profile_serializer.data,
    })


@api_view(['PUT'])
def update_profile(request):
    profile = Profile.objects.get(user=request.user)

    serializer = ProfileSerializer(
        profile,
        data=request.data
    )

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)