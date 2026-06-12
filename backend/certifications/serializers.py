from rest_framework import serializers

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        # model = Certification
        fields = '__all__'