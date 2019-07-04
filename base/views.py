import operator
from math import cos, sin, acos, sqrt
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from rest_framework.views import APIView
from .models import Member
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from base.serializer import MemberSerializerSignup, LoginSerializer, ConditionChangeSerializer, LocationChangeSerializer


def home(request, format=None):
    # query = Member.objects.all()
    authentication_classes(TokenAuthentication, )
    print(request.user)
    if request.user:
        return JsonResponse({"Hello": str(request.user.username)}, safe=True)
    else:
        return JsonResponse({"Please": "login First"}, safe=True)


@api_view(['GET'])
def members_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Member.objects.all()
        serializer = MemberSerializerSignup(snippets, many=True)  # Todo: Have to Change the serializer!
        return JsonResponse(serializer.data, safe=False)


# @api_view(['POST'])
# def doctors_signup(request, format=None):
#     # request.method == 'POST'
#     data = JSONParser().parse(request)
#     serializer = DoctorSerializerSignup(data=data)
#     if serializer.is_valid():
#         serializer.save()
#         # Doctor.objects.create(username=serializer.data['username'], password=serializer.data['password'],
#         #                       first_name=serializer.data['first_name'], last_name=serializer.data['username'],
#         #                       email=serializer.data['email'])
#         return JsonResponse(serializer.data, status=201)
#     return JsonResponse(serializer.errors, status=400)


@api_view(['POST'])
def signup(request, format=None):
    # request.method == 'POST'
    data = JSONParser().parse(request)
    serializer = MemberSerializerSignup(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        print(user.is_authenticated, user)
        django_login(request, user)
        token, create = Token.objects.get_or_create(user=user)  # user=settings.AUTH_USER_MODEL

        if user.is_authenticated:
            print("user is logined")
        else:
            print("no")

        return JsonResponse({'token': token.key, 'created': create}, safe=False, status=200)
        # return Response({"token": token.key}, status= 200)
# @api_view(['POST'])
# def member_login(request, format=None):
#     data = JSONParser().parse(request)
#     serializer = MemberSerializerLogin(data=data)
#     if serializer.is_valid():
#         print("I am here!")
#         if Member.objects.filter(username=serializer.data['username']).exists():
#              print("fuck you motherfucker")
#         username = serializer.data['username']
#         password = serializer.data['password']
#         print(username, password)
#         user = authenticate(username=username, password=password)
#         print(user)
#         if user:
#             login(request, user)
#             return JsonResponse(serializer.data, status=201)
#         else:
#             return JsonResponse({"error": "We do not have this user!"}, status=404)
#     return JsonResponse(serializer.errors, status=400)


class LogoutView(APIView):
    def post(self, request):
        authentication_classes(TokenAuthentication, )
        print("log out", request.user)
        django_logout(request)
        return redirect(reverse_lazy("home"))
        # return Response(status=204)


@api_view(['POST'])
def change_condition(request, format=None):
    # data = JSONParser().parse(request)
    # if request.user.is_authenticated:
    #     print('yes!')
    serializer = ConditionChangeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    member_set = list(Member.objects.filter(username=request.user.username))
    member = member_set[0]
    member.set_condition(state=serializer.data['condition'])
    return JsonResponse({"Condition": member.bad_or_busy_condition},
                        safe=False)


@api_view(['POST'])
def change_location(request, format=None):
    serializer = LocationChangeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    member_qset = Member.objects.filter(username=request.user.username)
    member = member_qset.first()
    member.set_location(longitude=serializer.data['longitude'],
                        latitude=serializer.data['latitude'],
                        altitude=serializer.data['altitude'])
    return JsonResponse({"Longitude": member.longitude,
                         "Latitude": member.latitude,
                         "Altitude": member.altitude})





def find_distance(patient, doctor):
    cos_tetha = sin(patient.latitude) * sin(doctor.latitude) + \
            cos(patient.latitude) * cos(doctor.latitude) * cos(patient.longitude - doctor.longitude)
    tetha = acos(cos_tetha)
    distance = sqrt(patient.altitude**2 + doctor.altitude**2 -
                    2 * patient.altitude * doctor.altitude * cos_tetha)
    return distance


@api_view(['POST'])
def find_doctor(request, format=None):
    patient_qset = Member.objects.filter(username=request.user.username)
    patient = patient_qset.first()
    doctors_distance = {}
    doctors_list = list(Member.objects.filter(is_doctor=True))
    for doctor in doctors_list:
        doctors_distance.update({doctor.id: find_distance(patient, doctor)})

    sorted_doctors = sorted(doctors_distance.items(), key=operator.itemgetter(1))
    # ToDO: NOW WE SHOULD CALL THE DOCTORS


