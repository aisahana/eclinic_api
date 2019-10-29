from rest_framework import serializers

from users.models import Doctor, Patient


class DoctorSerializer(serializers.ModelSerializer):
    poly_name = serializers.SerializerMethodField()

    def get_poly_name(self, obj):
        if obj.poly:
            return obj.poly.name
        return ''

    class Meta:
        model = Doctor
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class VisitorSerializer(serializers.ModelSerializer):
    visitor = serializers.IntegerField()
    class Meta:
        model = Patient
        fields = '__all__'