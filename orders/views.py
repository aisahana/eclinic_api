from django.db.models import Count
from django.utils.datetime_safe import datetime
import datetime as dtn
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders.models import Register
from orders.serializers import RegisterSerializer, CheckPatientSerializer


class RegisterViewSet(viewsets.ModelViewSet):
    serializer_class = RegisterSerializer
    queryset = Register.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    search_fields = [
        'register_number',
        'patient__patient_number',
        'patient__name',
        'doctor__doctor_number',
        'doctor__name',
        'poly__poly_number',
        'poly__name',
    ]
    filterset_fields = [
        'is_open',
        'is_draft',
        'patient',
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

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        register = self.get_object()
        register.is_draft = False
        register.save()

        return Response(
            self.get_serializer(register, many=False).data
        )

    @action(detail=False, methods=['post'])
    def check_patient(self, request):
        serializer = CheckPatientSerializer(data=request.data)
        if serializer.is_valid():
            registers = Register.objects.filter(
                patient__pk=serializer.data.get('patient_id'),
                is_open=True
            )
            if registers:
                raise ValidationError(
                    detail='Patient already registered now!',
                    code=status.HTTP_400_BAD_REQUEST
                )

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def total_open(self, request):
        registers = self.get_queryset().filter(
            is_open=True,
            is_draft=False,
            created__date=datetime.now().date()
        ).aggregate(Count('id'))

        return Response(dict(registers))

    @action(methods=['post'], detail=True)
    def close(self, request, pk=None):
        register = self.get_object()
        register.is_open = False
        register.save()

        return Response(self.serializer_class(register, many=False).data)

    @action(detail=False, methods=['get'])
    def report(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        registers = queryset.values_list(
            'register_number',
            'created__date',
            'patient__name',
            'doctor__name',
            'poly__name',
            'complain',
        )

        data = {
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
                    'text': 'LAPORAN REGISTRASI',
                    'fontSize': 20,
                    'margin': [0, 15]
                },
                {
                    'table': {
                        'body': [
                            [
                                'Nomer Registrasi',
                                'Tanggal',
                                'Pasien',
                                'Dokter',
                                'Poli',
                                'Keluhan'
                            ],
                            *registers
                        ]
                    }
                }
            ]
        }

        return Response(data)
