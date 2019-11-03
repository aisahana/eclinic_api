from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from counters.models import Counter, Queue
from counters.serializers import CounterSerializer, QueueSerializer, GenerateQueueSerializer
from utils.views import generate_queue


class CounterViewSet(viewsets.ModelViewSet):
    serializer_class = CounterSerializer
    queryset = Counter.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    ordering_fields = ['created',]
    search_fields = [
        'counter_number',
        'name',
    ]
    filterset_fields = [
        'is_draft',
    ]

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        counter = self.get_object()
        counter.is_draft = False
        counter.save()

        return Response(self.get_serializer(counter, many=False).data)

    @action(detail=True, methods=['post'])
    def draft(self, request, pk=None):
        counter = self.get_object()
        counter.is_draft = True
        counter.save()

        return Response(self.get_serializer(counter, many=False).data)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def public(self, request):
        queryset = self.get_queryset().filter(is_draft=False)
        return Response(self.get_serializer(queryset, many=True).data)


class QueueViewSet(viewsets.ModelViewSet):
    serializer_class = QueueSerializer
    queryset = Queue.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    ordering_fields = ['created',]
    search_fields = [
        'counter__counter_number',
        'counter__counter_name',
        'number',
    ]
    filterset_fields = [
        'is_draft',
        'is_complete',
    ]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def generate(self, request):
        serializer = GenerateQueueSerializer(data=request.data)
        if serializer.is_valid():
            queue = serializer.save()
            queue = generate_queue(queue.counter, queue)
            return Response(self.get_serializer(queue, many=False).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def next_number(self, request, pk=None):
        queue = self.get_object()
        queue.is_complete = True
        queue.save()

        return Response(self.get_serializer(queue, many=False).data)