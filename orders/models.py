from django.db import models

from polyclinics.models import Poly
from users.models import Patient, Doctor
from utils.models import Timestamp, auto_number


class Register(Timestamp):
    register_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    patient = models.ForeignKey(Patient, blank=True, null=True, on_delete=models.SET_NULL)
    complain = models.TextField(blank=True, null=True)
    poly = models.ForeignKey(Poly, blank=True, null=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(Doctor, blank=True, null=True, on_delete=models.SET_NULL)
    is_open = models.BooleanField(default=True)
    is_draft = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.register_number:
            self.register_number = auto_number('REG')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.register_number
