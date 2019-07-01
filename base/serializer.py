from django.contrib.auth import authenticate
from rest_framework import serializers as se

from base.models import Member  # Doctor, Patient
from rest_framework import exceptions


# class DoctorSerializerSignup(se.ModelSerializer):
#     class Meta:
#         model = Doctor
#         fields = ('id', 'first_name', 'last_name', 'username', 'password', 'email',
#                   'latitude', 'longitude', 'altitude')


class MemberSerializerSignup(se.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'email',
                  'is_doctor', 'bad_or_busy_condition')


# class MemberSerializerLogin(se.Serializer):
#     username = se.CharField(max_length=128)
#     password = se.CharField(max_length=256)
    # fields = ('username', 'password')


class LoginSerializer(se.Serializer):
    username = se.CharField()
    password = se.CharField()

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')

        if username and password:
            # user = authenticate(username=username, password=password)
            userSet = Member.objects.filter(username=username, password=password)
            if userSet:
                user = userSet[0]
            else:
                user = None
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    msg = 'user is deactivated!'
                    raise (exceptions.ValidationError(msg))
            else:
                print("user is" , user)
                msg = "Username or Password is Wrong!"
                raise (exceptions.ValidationError(msg))
        else:
            msg = "username and password required!"
            raise(exceptions.ValidationError(msg))

        return data


class ConditionChangeSerializer(se.Serializer):
    condition = se.CharField(max_length=5)






