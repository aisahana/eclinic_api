from rest_framework import serializers

from ehospitals.models import Kit, Drug, Action, Room, Enrollment, Treatment, TreatmentKit, TreatmentDrug, \
    TreatmentAction, TreatmentDoctor, PaymentHospital


class KitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kit
        fields = '__all__'


class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = '__all__'


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'


class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = '__all__'


class TreatmentKitSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentKit
        fields = '__all__'


class TreatmentDrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentDrug
        fields = '__all__'


class TreatmentActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentAction
        fields = '__all__'


class TreatmentDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentDoctor
        fields = '__all__'


class PaymentHospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHospital
        fields = '__all__'

