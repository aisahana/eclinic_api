from rest_framework import serializers

from medicines.models import Medicine, Recipe, RecipeItem
from payments.models import Payment


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'


class TotalUsedSerializer(serializers.ModelSerializer):
    total_used = serializers.IntegerField()
    total_amount = serializers.IntegerField()

    class Meta:
        model = Medicine
        fields = '__all__'


class MedicineCalculationSerializer(serializers.Serializer):
    current_quantity = serializers.IntegerField(required=True)
    new_quantity = serializers.IntegerField(required=True)


class RecipeSerializer(serializers.ModelSerializer):
    register_number = serializers.SerializerMethodField()
    doctor_number = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    patient_number = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()
    patient = serializers.SerializerMethodField()
    is_open = serializers.SerializerMethodField()
    sub_total = serializers.SerializerMethodField()
    doctor_fee = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    payment = serializers.SerializerMethodField()
    invoice = serializers.SerializerMethodField()

    def get_payment(self, obj):
        try:
            return Payment.objects.get(recipe=obj).pk
        except:
            return None

    def get_total(self, obj):
        return self.get_sub_total(obj) + self.get_doctor_fee(obj)

    def get_doctor_fee(self, obj):
        if obj.register:
            if obj.register.doctor:
                return obj.register.doctor.price
        return 0

    def get_sub_total(self, obj):
        total = sum([
            recipe_item.quantity * recipe_item.price
        for recipe_item in RecipeItem.objects.filter(recipe=obj, is_draft=False)])
        return total

    def get_register_number(self, obj):
        if obj.register:
            return obj.register.register_number
        return None

    def get_doctor_number(self, obj):
        if obj.register:
            if obj.register.doctor:
                return obj.register.doctor.doctor_number
        return None

    def get_doctor_name(self, obj):
        if obj.register:
            if obj.register.doctor:
                return obj.register.doctor.name
        return None

    def get_doctor(self, obj):
        if obj.register:
            if obj.register.doctor:
                return obj.register.doctor.pk
        return None

    def get_patient_number(self, obj):
        if obj.register:
            if obj.register.patient:
                return obj.register.patient.patient_number
        return None

    def get_patient_name(self, obj):
        if obj.register:
            if obj.register.patient:
                return obj.register.patient.name
        return None

    def get_patient(self, obj):
        if obj.register:
            if obj.register.patient:
                return obj.register.patient.pk
        return None

    def get_is_open(self, obj):
        if obj.register:
            return obj.register.is_open
        return None

    def get_invoice(self, obj):
        recipe_number = ['Kode Resep', obj.recipe_number]
        date = ['Tanggal', obj.created]
        patient = ['', '']
        poly = ['', '']
        doctor = ['', '']

        recipe_items = obj.recipeitem_set.all().values_list(
            'name',
            'unit',
            'medicine__medicine_type',
            'unfulfilled',
            'quantity'
        )

        recipe_item_columns = [
            'Nama Obat',
            'Satuan',
            'Jenis',
            'Tidak Terpenuhi',
            'Jumlah Terpenuhi',
        ]

        tables = [
            recipe_item_columns,
        ]
        for ri in recipe_items:
            tables.append(list(ri))

        if obj.register:
            if obj.register.patient:
                patient = ['Pasien', obj.register.patient.name]
            if obj.register.poly:
                poly = ['Poli', obj.register.poly.name]
            if obj.register.doctor:
                doctor = ['Dokter', obj.register.doctor.name]


        data = {
            'content': [
                {
                    'text': 'Resep',
                    'style': 'header',
                    'margin': [0, 20]
                },
                {
                    'columns': [
                        {
                            'layout': 'noBorders',
                            'table': {
                                'body': [
                                    recipe_number,
                                    date,
                                    patient
                                ]
                            }
                        },
                        {
                            'layout': 'noBorders',
                            'table': {
                                'body': [
                                    poly,
                                    doctor,
                                ]
                            }
                        }
                    ]
                },
                {
                    'margin': [0, 10],
                    'table': {
                        'body': tables
                    }
                }
            ]
        }
        return data


    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeItemSerializer(serializers.ModelSerializer):
    medicine_number = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    def validate(self, data):
        quantity = data.get('quantity')
        if quantity <= 0:
            raise serializers.ValidationError('Nilai jumlah/kuantitas tidak diterima!')
        return data

    def get_medicine_number(self, obj):
        if obj.medicine:
            return obj.medicine.medicine_number
        return None

    def get_total(self, obj):
        return obj.price * obj.quantity

    class Meta:
        model = RecipeItem
        fields = '__all__'

