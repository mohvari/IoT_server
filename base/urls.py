from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns

from base import views

urlpatterns = [
    path('members/', views.members_list, name='doctors-list'),
    # path('/lists/patients/', views.patients_list, name='patients-list'),

    path('signup/', views.signup, name='signup'),

    path('login/', views.LoginView.as_view(), name="login-view-class"),
    path('logout/', views.LogoutView.as_view(), name="logout-view-class"),
    path('change_condition/', views.change_condition, name="change-condition"),
    path('change_location/', views.change_location, name="change-location"),




    # path('patients/signup/', views.patients_signup,  name='patient-signup'),
    # path('login/', views.member_login, name='login'),
    # path('patients/', ,name='patients'),
    # path('doctors/api-token-auth/', obtain_auth_token, name='api_token_auth'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
