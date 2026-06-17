from rest_framework import serializers
from .models import User, Profile
from dj_rest_auth.registration.serializers import RegisterSerializer


class UserSerializer(RegisterSerializer):
    nickname = serializers.CharField()
    gender = serializers.ChoiceField(choices=User._meta.get_field('gender').choices)
    birth = serializers.DateField()
    profile_image = serializers.ImageField(required=False, allow_null=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname')
        data['gender'] = self.validated_data.get('gender')
        data['birth'] = self.validated_data.get('birth')
        data['profile_image'] = self.validated_data.get('profile_image')
        return data
    
    def save(self, request):
        user = super().save(request)

        user.nickname = self.validated_data.get('nickname')
        user.gender = self.validated_data.get('gender')
        user.birth = self.validated_data.get('birth')
        user.profile_image = self.validated_data.get('profile_image')
        user.save()

        Profile.objects.create(user=user)

        return user


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