from rest_framework import serializers
from .models import Competition

class CompetitionSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Competition
        fields = '__all__'