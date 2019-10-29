from rest_framework import serializers

from polyclinics.models import Poly


class PolySerializer(serializers.ModelSerializer):
    class Meta:
        model = Poly
        fields = '__all__'
