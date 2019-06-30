from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from base.models import Doctor
from base.serializer import PatientSerializerSignup, DoctorSerializerSignup, MemberSerializerLogin


@api_view(['GET'])
def doctors_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Doctor.objects.all()
        serializer = DoctorSerializerSignup(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def doctors_signup(request, format=None):
    # request.method == 'POST'
    data = JSONParser().parse(request)
    serializer = DoctorSerializerSignup(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


@api_view(['POST'])
def patients_signup(request, format=None):
    # request.method == 'POST'
    data = JSONParser().parse(request)
    serializer = PatientSerializerSignup(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


@api_view(['POST'])
def member_login(request, format=None):
    data = JSONParser().parse(request)
    serializer = MemberSerializerLogin(data=data)
    if serializer.is_valid():
        print("I am here!")
        username = serializer.data['username']
        password = serializer.data['password']
        print(username, password)
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse({"error": "We do not have this user!"}, status=404)
    return JsonResponse(serializer.errors, status=400)






