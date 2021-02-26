from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from . import serializers
import json
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts import usercontroller
from accounts.handler import check_email_is_valid
from django.contrib.auth import get_user_model
from rest_framework import generics
# This method will return the currently active user model the custom user model if one is specified, or User otherwise.
User = get_user_model()


class AddNewUser(APIView):
    """
    Handles Adding a User and returns the added user details
    """
    def post(self, request):
        # received_json_data = json.loads(request.body)
        # user_name = received_json_data['username']
        # email = received_json_data['email']
        # first_name = received_json_data['first_name']
        # if not check_email_is_valid(email):
        #     return Response({"data":"","success":False,"error" :"not a valid email"})
        # if user_name == None or user_name == "":
        #     return Response({"data":"","success":False,"error":"Username cannot be empty"})
        # if email== None or email == "":
        #     return Response({"data":"","success":False, "error": "Email cannot be empty"})
        # if  first_name == None or first_name == "":
        #     return Response({"data":"","success":False,"error":"first_name cannot be empty"})
        data = usercontroller.add_user(request)
        # except ValueError:
        #     return Response({"data":"","success" : False,"error" : "username already exist"})
        # except (AttributeError, IOError) as e:
        #     return Response({"data":"","success" : False,"error" : "Email or details are invalid"})
        # except Exception as e:
        #     return Response({'data':'','success':True,'error':str(e)})
        return Response(data)


class GetAllUser(APIView):
    """
    Retreive List of users
    """
    def get(self, request):
        data = usercontroller.get_all_users()
        return Response(data)


class ValidateUser(APIView):
    """
    an endpoint for validating User
    """
    permission_classes = (AllowAny,)

    def post(self,request):
            # info = request.body.decode('utf-8')
            # received_json_data = json.loads(info)
            # # username = request.POST.get("username")
            # # password = request.POST.get("password")
            # username = received_json_data.get("username")
            # password = received_json_data.get("password")
            # if not username:
            #     return JsonResponse({"data": "", "success":False, "error": "username or password cannot be Empty"})
            # if password == "" or password is None:
            #     return JsonResponse({"data": "", "success": False, "error": "Password cannot be empty"})
        try:
            response = usercontroller.validate_user(request)
        except ValueError as e:
            error = str(e)
            return Response({"data": "", "success": False, "error": error})
        return Response(response)


class UpdateUser(APIView):
    """
    An endpoint for updating user
    """
    permission_classes = (IsAuthenticated,)

    def patch(self,request,id):
        data = usercontroller.update_user(request,id)
        return Response(data)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = serializers.ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({'data':'','success':False,'error':'Wrong Old Password'})
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'data': 'Password updated successfully',
                'success': True,
                'error':'',
            }

            return Response(response)

        return Response(serializer.errors)


class UserDetail(APIView):

    def get(self,request,id):
        user = usercontroller.userdetail(request,id)
        return Response({'data': user, 'success': True, 'error': ''})


class Logout(APIView):
    def post(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response({'data':'User Logged Out','success':True,'error':''})


# ------------------- Roles CRUD ------------------------#


class GetAllRoles(APIView):
    def get(self,request):
        data = usercontroller.get_all_roles()
        return Response(data)


class AddNewRole(APIView):
    def post(self,request):
        # role_id = request.POST.get("role_id")
        # role_name = request.POST.get("role_name")
        # role_desc = request.POST.get("role_desc")

        data = usercontroller.add_role(request)
        return Response(data)

# # ---------- CRUD operation for Office -----------


class OfficeList(APIView):

    def post(self,request):
        data = usercontroller.add_office(request)
        return Response(data)

    def get(self,request):
        data = usercontroller.get_all_office(request)
        return Response(data)


class OfficeDetail(APIView):

    def get(self, request, pk):
        data = usercontroller.get_office_detail(request,pk)
        return Response(data)

    def put(self,request,pk):
        data = usercontroller.update_office(request,pk)
        return Response(data)

    def delete(self,request,pk):
        data = usercontroller.delete_office(request,pk)
        return Response(data)


# -------- CRUD operation for Designation -------------


class DesignationList(APIView):

    def post(self,request):
        data = usercontroller.add_designation(request)
        return Response(data)

    def get(self,request):
        data = usercontroller.get_all_designation(request)
        return Response(data)


class DesignationDetail(APIView):

    def put(self,request,pk):
        data = usercontroller.update_designation(request,pk)
        return Response(data)

    def get(self,request,pk):
        data = usercontroller.get_designation_detail(request,pk)
        return Response(data)

    def delete(self,request,pk):
        data = usercontroller.delete_designation(request,pk)
        return Response(data)


# -------- CRUD operation for Division -------------

# class DivisionList(APIView):
#
#     def post(self, request):
#         data = usercontroller.add_division(request)
#         return Response(data)
#
#     def get(self,request):
#         data = usercontroller.get_all_division(request)
#         return Response(data)
#
#
# class DivisionDetail(APIView):
#
#     def put(self,request,pk):
#         data = usercontroller.update_division(request,pk)
#         return Response(data)
#
#     def delete(self,request,pk):
#         data = usercontroller.delete_division(request,pk)
#         return Response(data)
#
#     def get(self,request):
#         data = usercontroller.get_division_detail()
#         return Response(data)



#--------------CRUD for PINCODE -------------------


# class PinCodeList(APIView):
#
#     def post(self, request):
#         data = add_pincode(request)
#         return JsonResponse(data)
#
#     def get(self,request):
#         data = get_all_pincode(request)
#         return JsonResponse(data)
#
#
#
# class PinCodeDetail(APIView):
#
#     def put(self,request,pk):
#         data = update_pincode(request,pk)
#         return JsonResponse(data)
#
#     def delete(self,request,pk):
#         data = delete_pincode(request,pk)
#         return JsonResponse(data)
#
#     def get(self,request,pk):
#         data = get_pincode_detail(request,pk)
#         return JsonResponse(data)



#-------------------CRUD for DISTRICT----------------------


class DistrictList(APIView):

    def post(self, request):
        data = usercontroller.add_district(request)
        return Response(data)

    def get(self, request):
        data = usercontroller.get_all_district(request)
        return Response(data)


class DistrictDetail(APIView):

    def put(self, request, pk):
        data = usercontroller.update_district(request, pk)
        return Response(data)

    def delete(self, request, pk):
        data = usercontroller.delete_district(request, pk)
        return Response(data)

    def get(self,request,pk):
        data = usercontroller.get_district_detail(request,pk)
        return Response(data)


# ---------------------CRUD FOR ARTICLE------------------------------------


class ArticleList(APIView):

    def post(self, request):
        data = usercontroller.add_article(request)
        return Response(data)

    def get(self, request):
        data = usercontroller.get_all_article(request)
        return Response(data)


class ArticleDetail(APIView):

    def put(self, request, pk):
        data = usercontroller.update_article(request, pk)
        return Response(data)

    def delete(self, request, pk):
        data = usercontroller.delete_article(request, pk)
        return Response(data)

    def get(self,request,pk):
        data = usercontroller.get_article_detail(request,pk)
        return Response(data)


