from rest_framework import serializers as se

from base.models import Doctor, Patient, Member


class DoctorSerializerSignup(se.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'email',
                  'latitude', 'longitude', 'altitude')


class MemberSerializerLogin(se.Serializer):
    username = se.CharField(max_length=128)
    password = se.CharField(max_length=256)
    # fields = ('username', 'password')


class PatientSerializerSignup(se.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'email',
                  'latitude', 'longitude', 'altitude')

