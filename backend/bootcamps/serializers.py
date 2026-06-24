from rest_framework import serializers
from .models import (
    Region,
    Skill,
    Bootcamp,
)
from jobs.models import Company


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class BootcampSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    region = RegionSerializer(read_only=True)
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Bootcamp
        fields = '__all__'


