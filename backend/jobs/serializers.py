from rest_framework import serializers
from .models import Company,Recruitment, RecruitmentDetail


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class RecruitmentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecruitmentDetail
        fields = '__all__'


class RecruitmentSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Recruitment
        fields = '__all__'


class RecruitmentDetailReadSerializer(serializers.ModelSerializer):
    company = CompanySerializer(
        source='recruitment.company',
        read_only=True,
    )

    recruitment = RecruitmentSerializer(
        read_only=True,
    )

    class Meta:
        model = RecruitmentDetail
        fields = '__all__'