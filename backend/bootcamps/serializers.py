from rest_framework import serializers
from .models import (
    Region,
    Skill,
    Bootcamp,
)


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = '__all__'


class BootcampSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    region = RegionSerializer(read_only=True)

    class Meta:
        model = Bootcamp
        fields = '__all__'


