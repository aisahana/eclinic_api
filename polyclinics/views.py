import json

from django.utils.datetime_safe import datetime
from rest_framework import viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from polyclinics.models import Poly
from polyclinics.serializers import PolySerializer


class PolyViewSet(viewsets.ModelViewSet):
    serializer_class = PolySerializer
    queryset = Poly.objects.all().order_by('is_draft', '-updated')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    search_fields = [
        'poly_number',
        'name',
    ]
    filterset_fields = ['is_draft']

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        poly = self.get_object()

        if not poly.name:
            raise ValidationError(
                detail='Nama poli tidak valid!',
                code=400
            )

        poly.is_draft = False
        poly.save()

        return Response(self.get_serializer(poly, many=False).data)

    @action(detail=False, methods=['get'])
    def report(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        print(queryset)
        polys = queryset.values_list(
            'poly_number',
            'name',
        )

        data = {
            'content': [
                {
                    'text': 'LAPORAN POLI',
                    'fontSize': 20,
                    'margin': [0, 15]
                },
                {
                    'text': f'Tanggal: {datetime.now().strftime("%d-%m-%Y")}',
                    'margin': [0, 15]
                },
                {
                    'table': {
                        'body': [
                            [
                                'Nomer Poli',
                                'Nama',
                            ],
                            *polys
                        ]
                    }
                }
            ]
        }

        return Response(data)



