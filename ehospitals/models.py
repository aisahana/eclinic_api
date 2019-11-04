from django.db import models

from users.models import Patient, Doctor
from utils.models import Timestamp, auto_number


class Kit(Timestamp):
    kit_number = models.CharField(max_length=100, blank=True, null=True, unique=True)
    name = models.CharField(max_length=100, default='ex: Stetoskop')
    rate = models.IntegerField(default=1)
    is_publish = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.kit_number:
            self.kit_number = auto_number('KIT')

        super().save(*args, **kwargs)

    def __str__(self):
        return self.kit_number


class Drug(Timestamp):
    drug_number = models.CharField(max_length=100, blank=True, null=True, unique=True)
    name = models.CharField(max_length=100, default='ex: Paracetamol')
    rate = models.IntegerField(default=1)
    is_publish = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.drug_number:
            self.drug_number = auto_number('OBT')

        super().save(*args, **kwargs)

    def __str__(self):
        return self.drug_number


class Action(Timestamp):
    action_number = models.CharField(max_length=100, blank=True, null=True, unique=True)
    name = models.CharField(max_length=100, default='ex: Infus')
    rate = models.IntegerField(default=1)
    is_publish = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.action_number:
            self.action_number = auto_number('ACT')

        super().save(*args, **kwargs)

    def __str__(self):
        return self.action_number


class Room(Timestamp):
    room_number = models.CharField(max_length=100, blank=True, null=True, unique=True)
    name = models.CharField(max_length=100, default='ex: Mawar')
    capacity = models.IntegerField(default=1)
    rate = models.IntegerField(default=1)
    fill = models.IntegerField(default=0)
    is_full = models.BooleanField(default=False)
    is_publish = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.room_number:
            self.room_number = auto_number('KMR')

        super().save(*args, **kwargs)

    def __str__(self):
        return self.room_number


class Enrollment(Timestamp):
    enrollment_number = models.CharField(max_length=100, blank=True, null=True, unique=True)
    enrollment_date = models.DateField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True)
    is_complete = models.BooleanField(default=False)
    is_publish = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.enrollment_number:
            self.enrollment_number = auto_number('REG')

        super().save(*args, **kwargs)

    def __str__(self):
        return self.enrollment_number


class Treatment(Timestamp):
    treatment_number = models.CharField(max_length=100, blank=True, null=True, unique=True)
    enrollment = models.ForeignKey(Enrollment, blank=True, null=True, on_delete=models.SET_NULL)
    treatment_date = models.DateField(auto_now_add=True)
    total = models.IntegerField(default=0)
    is_publish = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.treatment_number:
            self.treatment_number = auto_number('RWT')

        super().save(*args, **kwargs)

    def __str__(self):
        return self.treatment_number


class TreatmentKit(Timestamp):
    treatment = models.ForeignKey(Treatment, blank=True, null=True, on_delete=models.CASCADE)
    kit = models.ForeignKey(Kit, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(default='ex: Your description')
    price = models.IntegerField(default=0)
    is_publish = models.BooleanField(default=True)


    def __str__(self):
        return self.kit.kit_number


class TreatmentDrug(Timestamp):
    treatment = models.ForeignKey(Treatment, blank=True, null=True, on_delete=models.CASCADE)
    kit = models.ForeignKey(Kit, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(default='ex: Your description')
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    is_publish = models.BooleanField(default=True)

    def __str__(self):
        return self.kit.kit_number


class TreatmentAction(Timestamp):
    treatment = models.ForeignKey(Treatment, blank=True, null=True, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(default='ex: Your description')
    price = models.IntegerField(default=0)
    is_publish = models.BooleanField(default=True)

    def __str__(self):
        return self.action.action_number


class TreatmentDoctor(Timestamp):
    treatment = models.OneToOneField(Treatment, blank=True, null=True, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(default='ex: Your description')
    price = models.IntegerField(default=0)
    is_publish = models.BooleanField(default=True)

    def __str__(self):
        return self.doctor.doctor_number


class PaymentHospital(Timestamp):
    payment_number = models.CharField(max_length=100, blank=True, null=True, unique=True)
    enrollment = models.OneToOneField(Enrollment, blank=True, null=True, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    pay = models.IntegerField(default=0)
    change = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    is_publish = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.payment_number:
            self.payment_number = auto_number('PAY')

        super().save(*args, **kwargs)

    def __str__(self):
        return self.payment_number



