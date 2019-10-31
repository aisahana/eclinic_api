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
from utils.views import pdf_template


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
        polys = queryset.values_list(
            'poly_number',
            'name',
        )
        body = {
            'table': {
                'widths': ['*', '*'],
                'body': [
                    [
                        {'text': 'Nomer Poli', 'style': 'tableHeader'},
                        {'text': 'Nama', 'style': 'tableHeader'},
                    ],
                    *polys
                ]
            }
        }
        template = pdf_template([body], 'Laporan Poli', orientation='landscape')

        return Response(template)



