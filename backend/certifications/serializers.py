from rest_framework import serializers
from .models import Certification, Examination


class ExaminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examination
        exclude = ['certification']


class CertificationSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    examinations = ExaminationSerializer(many=True, read_only=True)

    class Meta:
        model = Certification
        fields = '__all__'


class CertificationDetailSerializer(serializers.ModelSerializer):
    examinations = ExaminationSerializer(many=True, read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)


    class Meta:
        model = Certification
        fields = '__all__'