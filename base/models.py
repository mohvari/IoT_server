from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractUser
from django.db import models

# class Member(AbstractUser):


class Member(AbstractUser):
    is_doctor = models.BooleanField(default=False)  # doctor = True, patient = False
    bad_or_busy_condition = models.BooleanField(default=False)
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)
    altitude = models.FloatField(default=0.0)

    def set_condition(self, state):
        if self.is_doctor:
            if state == "free":
                self.bad_or_busy_condition = False
            else:
                self.bad_or_busy_condition = True
        else:
            if state == "bad":
                self.bad_or_busy_condition = True
            else:
                self.bad_or_busy_condition = False
