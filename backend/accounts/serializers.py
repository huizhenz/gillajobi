from rest_framework import serializers
from .models import User, Profile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'email',
            'nickname',
            'gender',
            'birth',
            'profile_image',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'education',
            'certification',
            'experience',
            'language',
            'preferred_location',
            'preferred_position',
            'desired_salary',
        )