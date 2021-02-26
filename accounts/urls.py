#
from django.urls import path,include
from rest_framework.authtoken.views import obtain_auth_token
from .userviews import *

import django_rest_passwordreset.urls

urlpatterns = [
    path('addUser/', AddNewUser.as_view()),
    path('getAllUser/', GetAllUser.as_view()),
    path('validateUser/', ValidateUser.as_view()),
    path('updateUser/<int:id>/',UpdateUser.as_view()),
    path('changePassword/', ChangePasswordView.as_view(), name='change-password'),
    path('passwordReset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('logout/', Logout.as_view()),

    path('addRole/', AddNewRole.as_view()),
    path('getAllRoles/', GetAllRoles.as_view()),

    path('offices/',OfficeList.as_view()),
    path('offices/<int:pk>',OfficeDetail.as_view()),


    path('Designations/',DesignationList.as_view()),
    path('Designations/<int:pk>',DesignationDetail.as_view()),


    # path('Divisions/',DivisionList.as_view()),
    # path('Divisions/<int:pk>',DivisionDetail.as_view()),
    # path('Pincodes/',PinCodeList.as_view()),
    # path('Pincodes/<int:pk>',PinCodeDetail.as_view()),

    path('Districts/',DistrictList.as_view()),
    path('Districts/<int:pk>',DistrictDetail.as_view()),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth')

]