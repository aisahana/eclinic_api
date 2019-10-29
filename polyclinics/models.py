from django.db import models

from utils.models import Timestamp, auto_number


class Poly(Timestamp):
    poly_number = models.CharField(unique=True, max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True,)
    is_draft = models.BooleanField(default=True)

    def __str__(self):
        return self.poly_number

    def save(self, *args, **kwargs):
        if not self.poly_number:
            self.poly_number = auto_number('POL')

        if not self.name:
            self.name = 'My Poly'

        super().save(*args, **kwargs)

