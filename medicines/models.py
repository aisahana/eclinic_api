from django.db import models

from orders.models import Register
from utils.models import Timestamp, auto_number


class Medicine(Timestamp):
    medicine_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    unit = models.CharField(max_length=100, blank=True, null=True)
    medicine_type = models.CharField(max_length=100, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    is_draft = models.BooleanField(default=True)

    def __str__(self):
        return self.medicine_number

    def save(self, *args, **kwargs):
        if not self.medicine_number:
            self.medicine_number = auto_number('MED')

        if not self.name:
            self.name = 'My Medicine'

        if not self.unit:
            self.unit = 'pcs'

        if not self.stock:
            self.stock = 1

        if not self.price:
            self.price = 1000

        if not  self.medicine_type:
            self.medicine_type = 'Tablet'

        super().save(*args, **kwargs)


class Recipe(Timestamp):
    recipe_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    register = models.ForeignKey(Register, blank=True, null=True, on_delete=models.SET_NULL)
    diagnosis = models.TextField(blank=True, null=True)
    action = models.TextField(blank=True, null=True)
    is_draft = models.BooleanField(default=True)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return self.recipe_number

    def save(self, *args, **kwargs):
        if not self.recipe_number:
            self.recipe_number = auto_number('RCP')
        super().save(*args, **kwargs)


class RecipeItem(Timestamp):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, blank=True, null=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    unit = models.CharField(max_length=100, blank=True, null=True)
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    unfulfilled = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    is_draft = models.BooleanField(default=True)

    def __str__(self):
        return self.medicine.medicine_number
