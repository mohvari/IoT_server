from django.contrib.auth.models import AbstractUser
from django.db import models

# class Member(AbstractUser):


class Member(AbstractUser):
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)
    altitude = models.FloatField(default=0.0)
    pass


class Doctor(Member):
    # image = models.ImageField(null=True)
    is_free = models.BooleanField(default=True)


class Patient(Member):
    in_bad_condition = models.BooleanField(default=False)
    pass


