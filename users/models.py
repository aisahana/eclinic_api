from django.contrib.auth.models import User
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.datetime_safe import datetime
from rest_framework.authtoken.models import Token

from polyclinics.models import Poly
from utils.models import Timestamp, auto_number


class Doctor(Timestamp):
    MALE = 'male'
    FEMALE = 'female'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female')
    )
    doctor_number = models.CharField(unique=True, blank=True, null=True, max_length=20)
    name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=MALE)
    phone = models.CharField(max_length=100, blank=True, null=True)
    price = models.PositiveIntegerField(default=0)
    poly = models.ForeignKey(Poly, on_delete=models.SET_NULL, blank=True, null=True)
    is_draft = models.BooleanField(default=True)

    def __str__(self):
        return self.doctor_number

    def save(self, *args, **kwargs):
        if not self.doctor_number:
            self.doctor_number = auto_number('DR')

        if not self.name:
            self.name = 'Dr. Aisah'

        if not self.gender:
            self.gender = self.FEMALE

        if not self.phone:
            self.phone = '+62'

        if not self.price:
            self.price = 100000

        super().save(*args, **kwargs)

class Patient(Timestamp):
    MALE = 'male'
    FEMALE = 'female'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female')
    )

    BLOOD_A = 'A'
    BLOOD_B = 'B'
    BLOOD_AB = 'AB'
    BLOOD_O = 'O'
    BLOOD_CHOICES = (
        (BLOOD_A, 'A'),
        (BLOOD_B, 'B'),
        (BLOOD_AB, 'AB'),
        (BLOOD_O, 'O'),
    )
    MUSLIM = 'muslim'
    CATHOLIC = 'catholic'
    PROTESTANT = 'protestant'
    HINDU = 'hindu'
    BUDDHA = 'buddha'
    CONFUCIUS = 'confucius'
    RELIGION_CHOICES = (
        (MUSLIM, 'Muslim'),
        (CATHOLIC, 'Catholic'),
        (PROTESTANT, 'Protestant'),
        (HINDU, 'Hindu'),
        (BUDDHA, 'Buddha'),
        (CONFUCIUS, 'Conficius'),
    )
    MARRIED = 'married'
    SINGLE = 'single'
    WIDOW = 'widow'
    WIDOWER = 'widower'
    MARITAL_CHOICES = (
        (MARRIED, 'Married'),
        (SINGLE, 'Single'),
        (WIDOW, 'Widow'),
        (WIDOWER, 'Widower'),
    )
    patient_number = models.CharField(unique=True, blank=True, null=True, max_length=20)
    name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=MALE)
    place_birth = models.CharField(max_length=100, blank=True, null=True)
    date_birth = models.DateField(blank=True, null=True)
    age = models.PositiveIntegerField(default=0)
    phone = models.CharField(max_length=100, blank=True, null=True)
    blood = models.CharField(max_length=10, choices=BLOOD_CHOICES, default=BLOOD_A)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    religion = models.CharField(max_length=100, choices=RELIGION_CHOICES, default=MUSLIM)
    marital = models.CharField(max_length=100, choices=MARITAL_CHOICES, default=MARRIED)
    is_draft = models.BooleanField(default=True)

    def __str__(self):
        return self.patient_number

    def save(self, *args, **kwargs):
        if not self.patient_number:
            self.patient_number = auto_number('PNT')

        if not self.name:
            self.name = 'Tn. Budiman'

        if not self.place_birth:
            self.place_birth = 'Jakarta'

        if not self.date_birth:
            self.date_birth = '2019-01-29'

        if not self.age:
            self.age = 30

        if not self.phone:
            self.phone = '0859999999999'

        if not self.occupation:
            self.occupation = 'Wiraswasta'

        if not self.religion:
            self.religion = self.MUSLIM

        if not self.marital:
            self.marital = self.SINGLE

        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
