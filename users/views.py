from django.db.models import Count, Sum
from django.utils.datetime_safe import datetime
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from medicines.models import Recipe
from orders.models import Register
from users.models import Doctor, Patient
from users.serializers import DoctorSerializer, PatientSerializer, VisitorSerializer


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username
        })


class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    search_fields = [
        'doctor_number',
        '$name',
        'phone',
        '$poly__name',
        'poly__poly_number'
    ]
    filterset_fields = [
        'is_draft',
        'poly',
    ]

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        doctor = self.get_object()
        doctor.is_draft = False
        doctor.save()

        return Response(self.get_serializer(doctor, many=False).data)

    @action(detail=False, methods=['get'])
    def report(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        doctors = queryset.values_list(
            'doctor_number',
            'name',
            'gender',
            'phone',
            'price',
            'poly__poly_number'
        )

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
                    'text': 'LAPORAN DOKTER',
                    'fontSize': 20,
                    'margin': [0, 15]
                },
                {
                    'layout': 'lightHorizontalLines',
                    'table': {
                        'body': [
                            [
                                'Nomer Dokter',
                                'Nama',
                                'Gender',
                                'Telepon',
                                'Tarif',
                                'Kode Poli',
                            ],
                            *doctors
                        ]
                    }
                }
            ]
        }

        return Response(data)


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    search_fields = [
        'patient_number',
        '$name',
        '=blood',
        '$phone'
    ]
    filterset_fields = [
        'is_draft',
    ]

    @action(methods=['post'], detail=True)
    def publish(self, request, pk=None):
        patient = self.get_object()
        patient.is_draft = False
        patient.save()

        return Response(self.get_serializer(patient, many=False).data)

    @action(methods=['get'], detail=False)
    def total_new(self, request):
        patients = self.get_queryset().filter(
            is_draft=False,
            created__date=datetime.now().date()
        ).aggregate(Count('id'))

        return Response(dict(patients))

    @action(methods=['get'], detail=False)
    def visitor(self, request):
        patients = Patient.objects\
            .filter(is_draft=False)\
            .annotate(visitor=Count('register', distinct=True)).distinct().order_by('-visitor')[:5]

        return Response(VisitorSerializer(patients, many=True).data)

    @action(detail=False, methods=['get'])
    def report(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        patients = queryset.values_list(
            'patient_number',
            'name',
            'gender',
            'place_birth',
            'date_birth',
            'phone',
            'occupation',
            'religion',
        )

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
                    'text': 'LAPORAN PASIEN',
                    'fontSize': 20,
                    'margin': [0, 15]
                },
                {
                    'layout': 'lightHorizontalLines',
                    'table': {
                        'body': [
                            [
                                'Nomer Pasien',
                                'Nama',
                                'Gender',
                                'Tempat Lahir',
                                'Tanggal Lahir',
                                'Telepon',
                                'Pekerjaan',
                                'Agama',
                            ],
                            *patients
                        ]
                    }
                }
            ]
        }

        return Response(data)

    @action(detail=True, methods=['post'])
    def report_medical_record(self, request, pk=None):
        patient = self.get_object()
        diagnosis = []
        recipes = Recipe.objects.filter(register__patient=patient)
        for recipe in recipes:
            date = recipe.created.strftime('%d/%m/%Y')
            doctor = recipe.register.doctor.name if recipe.register.doctor else ''
            poly = recipe.register.poly.name if recipe.register.poly else ''
            complain = recipe.register.complain
            diagnosa = recipe.diagnosis
            act = recipe.action

            diagnosis.append({
                'layout': 'lightHorizontalLines',
                'table': {
                    'body': [
                        ['Tanggal', ':', date],
                        ['Dokter', ':', doctor],
                        ['Poli', ':', poly],
                        ['Keluhan', ':', complain],
                        ['Diagnosa', ':', diagnosa],
                        ['Tindakan', ':', act],
                    ]
                },
            })
            diagnosis.append('\n\n')

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
                    'text': 'REKAM MEDIS',
                    'fontSize': 20,
                    'margin': [0, 15]
                },
                {
                    'columns': [
                        {
                            'layout': 'noBorders',
                            'table': {
                                'body': [
                                    ['Nomer Pasien', ':', patient.patient_number],
                                    ['Nama', ':', patient.name],
                                    ['Alamat', ':', patient.address],
                                    ['Gender', ':', patient.gender],
                                    ['Tempat dan Tanggal Lahir', ':', f'{patient.place_birth}, {patient.date_birth}'],
                                ]
                            }
                        },
                        {
                            'layout': 'noBorders',
                            'table': {
                                'body': [
                                    ['Telepon', ':', patient.phone],
                                    ['Golongan Darah', ':', patient.blood],
                                    ['Pekerjaan', ':', patient.occupation],
                                    ['Status Pernikahan', ':', patient.marital],
                                ]
                            }
                        }
                    ],
                },
                '\n',
                *diagnosis
            ]
        }

        return Response(data)