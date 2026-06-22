from rest_framework import serializers
from .models import (
    Company,
    Recruitment,
    RecruitmentDetail,
    HiringProcess,
)


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class HiringProcessSerializer(serializers.ModelSerializer):

    class Meta:
        model = HiringProcess
        fields = '__all__'


class RecruitmentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecruitmentDetail
        fields = '__all__'


class RecruitmentListSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Recruitment
        fields = '__all__'


class RecruitmentDetailReadSerializer(serializers.ModelSerializer):
    company = CompanySerializer(
        source='recruitment.company',
        read_only=True
    )

    recruitment = RecruitmentListSerializer(
        read_only=True
    )

    processes = HiringProcessSerializer(
        source='recruitment.processes',
        many=True,
        read_only=True
    )

    class Meta:
        model = RecruitmentDetail
        fields = '__all__'