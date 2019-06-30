from rest_framework import serializers as se

from base.models import Doctor, Patient, Member


class DoctorSerializerSignup(se.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'email',
                  'latitude', 'longitude', 'altitude')


class UserSerializerLogin(se.ModelSerializer):
    class Meta:
        model = Member
        fields = ('username', 'password')


class PatientSerializerSignup(se.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'email',
                  'latitude', 'longitude', 'altitude')

