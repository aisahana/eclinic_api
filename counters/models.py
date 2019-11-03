from django.db import models

from utils.models import Timestamp, auto_number


class Counter(Timestamp):
    counter_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    name = models.CharField(max_length=100, default='Ex: Nama Loket')
    is_draft = models.BooleanField(default=True)

    def __str__(self):
        return self.counter_number

    def save(self, *args, **kwargs):
        if not self.counter_number:
            self.counter_number = auto_number('LKT')

        super().save(*args, **kwargs)


class Queue(Timestamp):
    counter = models.ForeignKey(Counter, on_delete=models.CASCADE)
    number = models.IntegerField(default=0)
    codec_time = models.DateField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=False)

    def __str__(self):
        return self.number

