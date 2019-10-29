from django.db import models

from medicines.models import Recipe
from utils.models import Timestamp, auto_number


class Payment(Timestamp):
    payment_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.PositiveIntegerField(default=0)
    pay = models.PositiveIntegerField(default=0)
    change = models.PositiveIntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=True)

    def __str__(self):
        return self.payment_number

    def save(self, *args, **kwargs):
        if not self.payment_number:
            self.payment_number = auto_number('PAY')
        super().save(*args, **kwargs)
