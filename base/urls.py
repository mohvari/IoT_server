from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns

from base import views

urlpatterns = [
    path('doctors/', views.doctors_list, name='doctors'),
    # path('doctors/api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('doctors/signup/', views.doctors_signup, name='doctor-signup'),
    path('patients/signup/', views.patients_signup,  name='patient-signup'),
    path('login/', views.member_login, name='login'),
    path('api/loginview/', views.LoginView.as_view(), name="login-view-class"),
    path('api/logoutview/', views.LogoutView.as_view(), name="logout-view-class"),
    path('patients/change_condition/', views.change_state, name="change-condition"),


    # path('patients/', ,name='patients'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
