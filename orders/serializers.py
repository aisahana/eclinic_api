from rest_framework import serializers

from medicines.models import Recipe
from orders.models import Register
from payments.models import Payment


class RegisterSerializer(serializers.ModelSerializer):
    doctor_number = serializers.SerializerMethodField()
    patient_number = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()
    poly_number = serializers.SerializerMethodField()
    recipe = serializers.SerializerMethodField()
    payment = serializers.SerializerMethodField()

    # This fields used for medical record
    doctor_name = serializers.SerializerMethodField()
    poly_name = serializers.SerializerMethodField()
    diagnosis = serializers.SerializerMethodField()
    action = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    def get_doctor_number(self, obj):
        if obj.doctor:
            return f'{obj.doctor.doctor_number} - {obj.doctor.name}'
        return None

    def get_poly_name(self, obj):
        if obj.poly:
            return obj.poly.name
        return None

    def get_diagnosis(self, obj):
        try:
            return Recipe.objects.get(register=obj).diagnosis
        except:
            return ''

    def get_action(self, obj):
        try:
            return Recipe.objects.get(register=obj).action
        except:
            return ''

    def get_date(self, obj):
        try:
            return obj.created.strftime('%d/%m/%Y')
        except:
            return ''

    def get_doctor_name(self, obj):
        if obj.doctor:
            return obj.doctor.name
        return None

    def get_patient_number(self, obj):
        if obj.patient:
            return f'{obj.patient.patient_number} - {obj.patient.name}'
        return None

    def get_patient_name(self, obj):
        if obj.patient:
            return obj.patient.name
        return None

    def get_poly_number(self, obj):
        if obj.poly:
            return f'{obj.poly.poly_number} - {obj.poly.name}'
        return None

    def get_recipe(self, obj):
        try:
            return Recipe.objects.get(register=obj).pk
        except:
            return None

    def get_payment(self, obj):
        try:
            recipe = Recipe.objects.get(register=obj)
            return Payment.objects.get(recipe=recipe).pk
        except:
            return None

    class Meta:
        model = Register
        fields = '__all__'


class CheckPatientSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField(required=True)