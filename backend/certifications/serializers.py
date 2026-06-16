from rest_framework import serializers
from .models import Certification, Examination

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'


class ExaminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examination
        exclude = ['certification']


class CertificationDetailSerializer(serializers.ModelSerializer):
    examinations = ExaminationSerializer(many=True, read_only=True)

    class Meta:
        model = Certification
        fields = '__all__'