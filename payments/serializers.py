from rest_framework import serializers

from payments.models import Payment
from utils.views import pdf_template


class PaymentSerializer(serializers.ModelSerializer):
    recipe_number = serializers.SerializerMethodField()
    register = serializers.SerializerMethodField()
    invoice = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()

    def get_patient_name(self, obj):
        if obj.recipe:
            if obj.recipe.register:
                if obj.recipe.register.patient:
                    return obj.recipe.register.patient.name
        return None

    def get_recipe_number(self, obj):
        if obj.recipe:
            return obj.recipe.recipe_number
        return None

    def get_register(self, obj):
        if obj.recipe:
            if obj.recipe.register:
                return obj.recipe.register.pk
        return None

    def get_invoice(self, obj):
        patient = ['', ':', '']
        doctor = ['', ':', '']
        poly = ['', ':', '']
        if obj.recipe:
            if obj.recipe.register:
                if obj.recipe.register.patient:
                    patient = ['Pasien', ':', obj.recipe.register.patient.name]
                if obj.recipe.register.doctor:
                    doctor = ['Dokter', ':', obj.recipe.register.doctor.name]
                if obj.recipe.register.poly:
                    poly = ['Poli', ':', obj.recipe.register.poly.name]

        body = {
            'layout': 'noBorders',
            'table': {
                'body': [
                    ['Nomer Pembayaran', ':', obj.payment_number],
                    ['Tanggal', ':', obj.created.strftime('%d-%m-%Y')],
                    patient,
                    doctor,
                    poly,
                    ['Biaya', ':', obj.amount],
                    ['Dibayar', ':', obj.pay],
                    ['Kembali', ':', obj.change],
                ]
            }
        }

        template = pdf_template([body], 'Faktur Pembayaran', orientation='landscape')

        return template

    class Meta:
        model = Payment
        fields = '__all__'

