from datetime import datetime

from rest_framework import serializers

from counters.models import Counter, Queue


class CounterSerializer(serializers.ModelSerializer):
    total_queue = serializers.SerializerMethodField()
    current_queue = serializers.SerializerMethodField()
    current_queue_id = serializers.SerializerMethodField()
    next_queue = serializers.SerializerMethodField()

    def get_total_queue(self, obj):
        queues = Queue.objects.filter(
            counter=obj,
            is_complete=False,
            is_draft=False,
            codec_time=datetime.now().date()
        ).count()

        return queues

    def get_current_queue(self, obj):
        queue = Queue.objects.filter(
            counter=obj,
            is_complete=False,
            is_draft=False,
            codec_time=datetime.now().date()
        ).first()
        if queue:
            return queue.number

        return 0

    def get_current_queue_id(self, obj):
        queue = Queue.objects.filter(
            counter=obj,
            is_complete=False,
            is_draft=False,
            codec_time=datetime.now().date()
        ).first()
        if queue:
            return queue.pk

        return None

    def get_next_queue(self, obj):
        queue = Queue.objects.filter(
            counter=obj,
            is_complete=False,
            is_draft=False,
            codec_time=datetime.now().date()
        ).first()
        queue_last = Queue.objects.filter(
            counter=obj,
            is_complete=False,
            is_draft=False,
            codec_time=datetime.now().date()
        ).last()

        if queue and queue_last:
            if queue.number == queue_last.number:
                return 0
            return queue.number + 1
        return 0

    class Meta:
        model = Counter
        fields = '__all__'


class QueueSerializer(serializers.ModelSerializer):
    counter_name = serializers.CharField(source='counter.name', read_only=True)

    class Meta:
        model = Queue
        fields = '__all__'


class GenerateQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = ['counter',]
