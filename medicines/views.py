import datetime as dtn
from django.db.models import Sum, F
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from medicines.models import Medicine, Recipe, RecipeItem
from medicines.serializers import MedicineSerializer, RecipeSerializer, RecipeItemSerializer, \
    MedicineCalculationSerializer, TotalUsedSerializer


class MedicineViewSet(viewsets.ModelViewSet):
    serializer_class = MedicineSerializer
    queryset = Medicine.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    ordering_fields = ['created',]
    search_fields = [
        'medicine_number',
        'name',
        'unit',
        'stock',
    ]
    filterset_fields = [
        'is_draft',
    ]

    @action(methods=['post'], detail=True)
    def publish(self, request, pk=None):
        medicine = self.get_object()
        medicine.is_draft = False
        medicine.save()

        return Response(self.get_serializer(medicine, many=False).data)

    @action(methods=['get'], detail=False)
    def total_used(self, request):
        medicines = self.get_queryset()\
            .filter(is_draft=False)\
            .annotate(
                total_used=Sum('recipeitem__quantity'),
                total_amount=Sum('recipeitem__quantity') * F('price')
        ).order_by('-total_used')[:5]

        return Response(TotalUsedSerializer(medicines, many=True).data)

    @action(detail=False, methods=['get'])
    def report(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        medicines = queryset.values_list(
            'medicine_number',
            'name',
            'unit',
            'medicine_type',
            'stock',
            'price',
        )

        data = {
            'content': [
                {
                    'text': 'LAPORAN OBAT',
                    'fontSize': 20,
                    'margin': [0, 15]
                },
                {
                    'table': {
                        'body': [
                            [
                                'Nomer Obat',
                                'Nama',
                                'Satuan',
                                'Jenis',
                                'Stok',
                                'Tarif'
                            ],
                            *medicines
                        ]
                    }
                }
            ]
        }

        return Response(data)


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filterset_fields = [
        'is_draft',
        'is_checked',
    ]
    search_fields = [
        'recipe_number',
        'register__register_number',
        'register__doctor__doctor_number',
        'register__doctor__name',
        'register__patient__patient_number',
        'register__patient__name',
    ]

    def get_queryset(self):
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        queryset = self.queryset

        if start_date and end_date:
            start_date = [int(i) for i in start_date.split('-')]
            end_date = [int(i) for i in end_date.split('-')]
            queryset = queryset.filter(created__range=(
                    dtn.date(*start_date),
                    dtn.date(*end_date)
                )
            )

        return queryset

    @action(methods=['post'], detail=True)
    def publish(self, request, pk=None):
        recipe = self.get_object()
        recipe.is_draft = False
        recipe.save()

        return Response(
            self.get_serializer(recipe, many=False).data
        )

    @action(methods=['post'], detail=True)
    def checked(self, request, pk=None):
        recipe = self.get_object()
        # Check stock quantity
        recipe_items = RecipeItem.objects.filter(recipe=recipe)
        if not recipe_items:
            raise ValidationError(
                detail='Item Obat masih kosong!',
                code=400
            )
        for ri in recipe_items:
            if ri.medicine:
                unfulfilled = ri.medicine.stock - ri.quantity
                stock = ri.medicine.stock
                if unfulfilled < 0:
                    ri.unfulfilled = abs(unfulfilled)
                    ri.quantity = stock
                    ri.save()
                    ri.medicine.stock = 0
                    ri.medicine.save()
                else:
                    ri.medicine.stock = ri.unfulfilled
                    ri.medicine.save()
                    ri.unfulfilled = 0
                    ri.save()

        recipe.is_checked = True
        recipe.save()

        return Response(
            self.get_serializer(recipe, many=False).data
        )

    @action(detail=False, methods=['get'])
    def report(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        print(queryset.count())

        data_contents = []
        for recipe in queryset:
            recipe_number = ['Nomer Resep', ':', recipe.recipe_number]
            date = ['Tanggal', ':', recipe.created.strftime('%d/%M/%Y')]
            patient = ['Pasien', ':', '']
            poly = ['Poli', ':', '']

            doctor = ['Dokter', ':', '']
            complain = ['Keluhan', ':', '']
            diagnosa = ['Diagnosa', ':', recipe.diagnosis]
            act = ['Tindakan', ':', recipe.action]

            if recipe.register:
                complain = ['Keluhan', ':', recipe.register.complain]

                if recipe.register.patient:
                    patient = ['Pasien', ':', recipe.register.patient.name]
                if recipe.register.poly:
                    poly = ['Poli', ':', f'{recipe.register.poly.poly_number} - {recipe.register.poly.name}']
                if recipe.register.doctor:
                    doctor = ['Dokter', ':', recipe.register.doctor.name]

            recipe_items = recipe.recipeitem_set.all().values_list(
                'medicine__name',
                'unit',
                'medicine__medicine_type',
                'quantity',
                'unfulfilled'
            )

            data_contents.append([
                { 'text': recipe.recipe_number, 'fontSize': 15 },
                '\n',
                {
                    'columns': [
                        {
                            'layout': 'noBorders',
                            'table': {
                                'body': [
                                    date,
                                    patient,
                                    poly
                                ]
                            }
                        }
                    ],
                },
                '\n',
                {
                    'layout': 'noBorders',
                    'table': {
                        'body': [
                            doctor,
                            complain,
                            diagnosa,
                            act
                        ]
                    }
                },
                '\n',
                {
                    'pageBreak': 'after',
                    'table': {
                        'body': [
                            [
                                'Nama Obat',
                                'Satuan',
                                'Jenis',
                                'Jumlah',
                                'Tidak Terpenuhi'
                            ],
                            *recipe_items
                        ]
                    }
                }
            ])

        data = {
            'pageOrientation': 'landscape',
            'watermark': {
                'text': 'eClinic - Aisahana',
                'color': 'blue',
                'opacity': 0.3,
                'bold': True,
                'italics': False,
                'fontSize': 60
            },
            'info': {
                'title': 'Aisahana Reporting',
                'author': 'Aisahana',
                'subject': 'Laporan Dokter',
            },
            'content': [
                {
                    'text': 'LAPORAN RESEP',
                    'fontSize': 20,
                    'margin': [0, 15]
                },
                *data_contents,
            ]
        }

        return Response(data)

class RecipeItemViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeItemSerializer
    queryset = RecipeItem.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_fields = [
        'recipe',
        'medicine',
        'price',
        'quantity',
        'is_draft',
    ]

    @action(methods=['post'], detail=True)
    def publish(self, request, pk=None):
        recipe_item = self.get_object()
        recipe_item.is_draft = False
        recipe_item.save()

        return Response(self.get_serializer(recipe_item, many=False).data)




