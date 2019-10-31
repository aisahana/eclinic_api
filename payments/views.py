import datetime as dtn
from django.db.models import Sum, F
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from payments.models import Payment
from payments.serializers import PaymentSerializer
from utils.views import pdf_template


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    search_fields = [
        'payment_number',
        'recipe__recipe_number',
    ]
    filterset_fields = [
        'is_paid',
        'is_draft'
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
                    dtn.date(*end_date) + dtn.timedelta(days=1)
                )
            )

        return queryset

    @action(methods=['post'], detail=True)
    def publish(self, request, pk=None):
        payment = self.get_object()
        payment.is_draft = False
        payment.save()

        return Response(
            self.get_serializer(payment, many=False).data
        )

    @action(methods=['get'], detail=False)
    def total_sale(self, request):
        summary = Payment.objects.filter(is_draft=False, is_paid=True).aggregate(
            Sum('amount')
        )
        return Response(dict(summary))

    @action(methods=['post'], detail=True)
    def paid(self, request, pk=None):
        payment = self.get_object()
        payment.is_paid = True
        payment.is_draft = False
        payment.save()

        return Response(
            self.get_serializer(payment, many=False).data
        )

    @action(detail=False, methods=['get'])
    def report(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        total = queryset.aggregate(total=Sum('amount'))
        payments = queryset.values_list(
            'payment_number',
            'created__date',
            'recipe__register__patient__name',
            'recipe__register__doctor__name',
            'recipe__register__poly__name',
            F('amount'),
        )

        body = [
            {
                'table': {
                    'body': [
                        [
                            'Nomer Pembayaran',
                            'Tanggal',
                            'Pasien',
                            'Dokter',
                            'Poli',
                            'Biaya'
                        ],
                        *payments
                    ]
                }
            },
            '\n',
            {'text': f'Total Rp. {total["total"]}', 'style': 'anotherStyle'}
        ]
        template = pdf_template([body], 'Laporan Pembayaran', orientation='landscape')
        return Response(template)