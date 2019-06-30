from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.views import APIView

from .models import Member
from django.contrib.auth import login as django_login, logout as django_logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from base.models import Doctor
from base.serializer import PatientSerializerSignup, DoctorSerializerSignup, \
    MemberSerializerLogin, LoginSerializer, ConditionChangeSerializer


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
        # Doctor.objects.create(username=serializer.data['username'], password=serializer.data['password'],
        #                       first_name=serializer.data['first_name'], last_name=serializer.data['username'],
        #                       email=serializer.data['email'])
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
        if Member.objects.filter(username=serializer.data['username']).exists():
             print("fuck you motherfucker")
        username = serializer.data['username']
        password = serializer.data['password']
        print(username, password)
        user = authenticate(username=username, password=password)
        print(user)
        if user:
            login(request, user)
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse({"error": "We do not have this user!"}, status=404)
    return JsonResponse(serializer.errors, status=400)




class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        token, create = Token.objects.get_or_create(user=user)
        return JsonResponse({'token': token.key, 'created': create}, safe=False, status=200)
        # return Response({"token": token.key}, status= 200)




def home(request):
    Response("logout successfully")


class LogoutView(APIView):
    authentication_classes(TokenAuthentication, )

    def post(self, request):
        django_logout(request)
        return redirect(reversed(""))
        # return Response(status=204)



@api_view(['POST'])
@login_required
def change_state(request):
    data = JSONParser().parse(request)
    serializer = ConditionChangeSerializer(data=data)
    request.user.set_condition(serializer.data['condition'])
    return JsonResponse({"Condition": ConditionChangeSerializer(data=data)},
                        safe=False)







