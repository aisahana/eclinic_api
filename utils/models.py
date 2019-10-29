from django.db import models
from django.utils.datetime_safe import datetime


class Timestamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def auto_number(prefix='PRD'):
    return datetime.now().strftime(f'{prefix}-%Y%m%d%H%M%S%f')
