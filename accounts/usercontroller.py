# from django.core.files.storage import FileSystemStorage
# from django.http import JsonResponse
# from django.db import IntegrityError
import json

from rest_framework.exceptions import ValidationError
from rest_framework.parsers import JSONParser
from .models import Office,Designation,District
from . import serializers
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model, login

User = get_user_model()
from post_office import mail
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token


def get_all_users():
    data = User.objects.all().order_by("treasury_code").values()
    serializer = serializers.UserSerializer(data,many=True)
    # print(serializer.data)
    return ({"data": serializer.data, "success": True, "error": ""})



def validate_user(request):
    print(request.data)
    serializer = serializers.LoginUserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        try:
            req_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValueError("User do not exist")
        if not req_user.check_password(password):
            raise ValueError("Password Mismatched")
        token,_ = Token.objects.get_or_create(user=req_user)
        userserializer = serializers.UserSerializer(req_user)
        # data = {'name': req_user.username, 'firstname': req_user.first_name, 'lastname': req_user.last_name,
        #    'email': req_user.email, 'user_id': req_user.id}
        login(request, req_user)
        return {'data':userserializer.data,'success':True,"error":"",'token':token.key}


def add_user(request):
    serializer = serializers.UserSerializer(data=request.data)
    # kwarg = dict(serializers.data)  # serializer.data is a dictionary
    # username = kwarg.pop("username")
    # email = kwarg.pop(("email"))
    try:
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            rand_password = User.objects.make_random_password()
            user = None
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                pass
            finally:
                if user is not None:
                    raise ValueError
            try:
                user = User.objects.get(username=username.lower())
            except User.DoesNotExist:
                pass
            finally:
                if user is not None:
                    raise ValueError
            password = make_password(rand_password)
            serializer.save(password=password)
            mail.send(
                [email, ],
                subject='Welcome',
                message=f"Hi your password is {rand_password}",
                priority='now',
            )
    except Exception as e:
        data = {'data':'','success':False,'error':str(e)}
    else:
        data = {'data':serializer.data,'success':True,'error':''}
    return data


def update_user(request,id):
    user = User.objects.get(treasury_code=id)
    serializer = serializers.UserSerializer(user,data=request.data,partial=True)
    try:
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return {'data':serializer.data,'success':True,'error':''}
    except Exception as e:
        return {'data':'','success':False,'error':str(e)}


def userdetail(request,id):
    user = User.objects.get(treasury_code=id)
    serializer = serializers.UserSerializer(user)
    return serializer.data


def add_role(request):
    serializer = serializers.AddRoleSerializer(data=request.data)
    # id = kwarg.pop("id")
    # name = kwarg.pop("name")
    # description = kwarg.pop("description")
    if serializer.is_valid():
        serializer.save()
    return ({"data": serializer.data, "success": True, "error": ""})


def get_all_roles():
    all_roles = Group.objects.all().order_by("id").values()
    serializer = serializers.AddRoleSerializer(all_roles,many=True)
    return {"data":serializer.data, "success": True, "error": ""}

# #-------------------------------------------------------------------


def add_office(request):
    data = JSONParser().parse(request)
    serializer = serializers.OfficeSerializer(data=data)
    print(serializer)
    try:
        if serializer.is_valid():
            serializer.save()
    except Exception as e:
        return {"data": " ", "success": False, "error": str(e)}
    return {"data": serializer.data, "success": True, "error": " "}


def get_all_office(request):
    try:
        data = list(Office.objects.filter(is_active=True).order_by('office_name').values())
    except Exception as e:
        print(str(e))
        return {"data": " ", "success": False, "error": str(e)}
    return {"data": data, "success": True, "error": " "}


def get_office_detail(request,pk):
    try:
        office = Office.objects.get(pk=pk)
        serializer = serializers.OfficeSerializer(office)
    except Office.DoesNotExist:
        return {"data": " ", "success": True, "error": "Office Does Not Exist"}
    except Exception as e:
        return {"data":" ","success":True,"error":str(e)}
    else:
        return {"data":serializer.data,"success":True,"error":" "}


def update_office(request, pk):
    try:
        office = Office.objects.get(pk=pk)
        data = JSONParser().parse(request)
        serializer = serializers.OfficeSerializer(office, data)
        if serializer.is_valid():
            serializer.save()
    except Office.DoesNotExist:
        return {"data": " ", "success": True, "error": "Office Does Not Exist"}
    except Exception as e:
        return {"data": " ", "success": False, "error": str(e)}
    else:
        return {"data": serializer.data, "success": True, "error": " "}


def delete_office(request, pk):
    try:
        office = Office.objects.get(pk=pk)
        office.is_active = False
        office.save()
    except Office.DoesNotExist:
        return {"data": " ", "success": True, "error": "Office Does Not Exist"}
    except Exception as e:
        return {"data": " ", "success": False, "error": str(e)}
    else:
        return {"data": " ", "success": True, "error": " "}









#----------------------------------------------------


def add_designation(request):
    try:
        data = JSONParser().parse(request)
        serializer = serializers.DesignationSerializer(data=data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
    except Exception as e:
        return {"data": " ", "success": False, "error": str(e)}
    return {"data": serializer.data, "success": True, "error": " "}


def get_all_designation(request):
    try:
        data = list(Designation.objects.filter(is_active=True).values())
    except Exception as e:
        return {"data": " ", "success": False, "error": str(e)}
    return {"data": data, "success": True, "error": " "}


def update_designation(request, pk):
    try:
        designation = Designation.objects.get(pk=pk)
        data = JSONParser().parse(request)
        serializer = serializers.DesignationSerializer(designation, data)
        if serializer.is_valid():
            serializer.save()
    except Designation.DoesNotExist:
        return {"data": " ", "success": True, "error": "Designation Does Not Exist"}
    except Exception as e:
        return {"data": " ", "success": False, "error": str(e)}
    else:
        return {"data": serializer.data, "success": True, "error": " "}


def get_designation_detail(request,pk):
    try:
        designation = Designation.objects.get(pk=pk)
        serializer = serializers.DesignationSerializer(designation)
    except Designation.DoesNotExist:
        return {"data": " ", "success": True, "error": "Designation Does Not Exist"}
    except Exception as e:
        return {"data": " ", "success": False, "error": str(e)}
    return {"data":serializer.data,"success":True,"error":" "}


def delete_designation(request, pk):
    try:
        designation = Designation.objects.get(pk=pk)
        designation.is_active = False
        designation.save()
    except Designation.DoesNotExist:
        return {"data": " ", "success": True, "error": "Designation Does Not Exist"}
    except Exception as e:
        return {"data": " ", "success": False, "error": str(e)}
    else:
        return {"data": " ", "success": True, "error": " "}


# -----------------------------------------------------------

# def add_division(request):
#     try:
#         data = JSONParser().parse(request)
#         serializer = serializers.DivisionSerializer(data=data)
#         print(serializer)
#         if serializer.is_valid():
#             serializer.save()
#     except Exception as e:
#         return {"data": " ", "success": False, "error": str(e)}
#     return {"data": serializer.data, "success": True, "error": " "}
#
#
# def get_all_division(request):
#     try:
#         data = list(Division.objects.filter(is_active=True).values())
#     except Exception as e:
#         return {"data": " ", "success": False, "error": str(e)}
#     return {"data": data, "success": True, "error": " "}
#
#
# def update_division(request, pk):
#     try:
#         designation = Division.objects.get(pk=pk)
#         data = JSONParser().parse(request)
#         serializer = DivisionSerializer(designation, data)
#         if serializer.is_valid():
#             serializer.save()
#     except Division.DoesNotExist:
#         return {"data": " ", "success": True, "error": "Division Does Not Exist"}
#     except Exception as e:
#         return {"data": " ", "success": False, "error": str(e)}
#     else:
#         return {"data": serializer.data, "success": True, "error": " "}
#
#
# def delete_division(request, pk):
#     try:
#         divison = Division.objects.get(pk=pk)
#         divison.is_active = False
#         divison.save()
#     except Division.DoesNotExist:
#         return {"data": " ", "success": True, "error": "Division Does Not Exist"}
#     except Exception as e:
#         return {"data": " ", "success": False, "error": str(e)}
#     else:
#         return {"data": " ", "success": True, "error": " "}
#
#
# def get_division_detail(request,pk):
#     try:
#         division = Division.objects.get(pk=pk)
#         serializer = DivisionSerializer(division)
#     except Division.DoesNotExist:
#         return {"data": " ", "success": True, "error": "Division Does Not Exist"}
#     except Exception as e:
#         return {"data":" ","success":False,"error":str(e)}
#     else:
#         return   {"data":serializer.data,"success":True,"error":" "}
#

#---------------------------------------------------------------------------


def add_district(request):
    try:
        data = JSONParser().parse(request)
        serializer = serializers.DistrictSerializer(data=data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
    except Exception as e:
        return {"data": " ", "success": False, "error": str(e)}
    return {"data": serializer.data, "success": True, "error": " "}


def get_all_district(request):
    try:
        data = list(District.objects.filter(is_active=True).values())
    except Exception as e:
        return {"data": " ", "success": False, "error": str(e)}
    return {"data": data, "success": True, "error": " "}


def update_district(request, pk):
    try:
        district = District.objects.get(pk=pk)
        data = JSONParser().parse(request)
        serializer = serializers.DistrictSerializer(district, data)
        if serializer.is_valid():
            serializer.save()
    except District.DoesNotExist:
        return {"data": " ", "success": True, "error": "District Does Not Exist"}
    except Exception as e:
        return {"data": " ", "success": False, "error": str(e)}
    else:
        return {"data": serializer.data, "success": True, "error": " "}


def delete_district(request, pk):
    try:
        district = District.objects.get(pk=pk)
        district.is_active = False
        district.save()
    except District.DoesNotExist:
        return {"data": " ", "success": True, "error": "District Does Not Exist"}
    except Exception as e:
        return {"data": " ", "success": False, "error": str(e)}
    else:
        return {"data": " ", "success": True, "error": " "}


def get_district_detail(request, pk):
    try:
        district = District.objects.get(pk=pk)
        serializer = serializers.DistrictSerializer(district)
    except District.DoesNotExist:
        return {"data": " ", "success": True, "error": "District Does Not Exist"}
    except Exception as e:
        return {"data": " ", "success": False, "error": str(e)}
    else:
        return {"data": serializer.data, "success": True, "error": " "}


#-------------------------------------------------------------------
#
# #
# # def add_pincode(request):
# #     try:
# #         data = JSONParser().parse(request)
# #         serializer = PinCodeSerializer(data=data)
# #         print(serializer)
# #         if serializer.is_valid():
# #             serializer.save()
# #     except Exception as e:
# #         return {"data": " ", "success": False, "error": str(e)}
# #     return {"data": serializer.data, "success": True, "error": " "}
# #
# #
# # def get_all_pincode(request):
# #     try:
# #         data = list(PinCode.objects.filter(is_active=True).values())
# #     except Exception as e:
# #         return {"data": " ", "success": False, "error": str(e)}
# #     return {"data": data, "success": True, "error": " "}
# #
# #
# # def update_pincode(request, pk):
# #     try:
# #         pincode = PinCode.objects.get(pk=pk)
# #         data = JSONParser().parse(request)
# #         serializer = PinCodeSerializer(pincode, data)
# #         if serializer.is_valid():
# #             serializer.save()
# #     except Exception as e:
# #         return {"data": " ", "success": False, "error": str(e)}
# #     else:
# #         return {"data": serializer.data, "success": True, "error": " "}
# #
# #
# # def delete_pincode(request, pk):
# #     try:
# #         pincode = PinCode.objects.get(pk=pk)
# #         pincode.is_active = False
# #         pincode.save()
# #     except Exception as e:
# #         return {"data": " ", "success": False, "error": str(e)}
# #     else:
# #         return {"data": " ", "success": True, "error": " "}
# #
# #
# # def get_pincode_detail(request,pk):
# #     try:
# #         division = PinCode.objects.get(pk=pk)
# #         serializer = PinCodeSerializer(division)
# #     except Exception as e:
# #         return {"data":" ","success":False,"error":str(e)}
# #     else:
# #         return  {"data":serializer.data,"success":True,"error":" "}
# #
#-----------------------------------------------------------------------------


def add_article(request):
    serializer = serializers.ArticleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return {'data':serializer.data,'success':True,'error':''}
    return {'data':'','success':False,'error':serializer.errors}


def get_all_article(request):
    articles = Article.objects.filter(is_active=True)
    serializer = serializers.ArticleSerializer(articles,many=True)
    if serializer.is_valid():
        return {'data':serializer.data,'success':True,'error':''}
    return {'data': '', 'success': False, 'error': serializer.errors}


def update_article(request, pk):
    try:
        article = Article.objects.get(pk=pk)
        data = JSONParser().parse(request)
        serializer = serializers.ArticleSerializer(article, data)
        if serializer.is_valid():
            serializer.save()
    except Article.DoesNotExist:
        return {"data": " ", "success": True, "error": "Article Does Not Exist"}
    except Exception as e:
        return {"data": " ", "success": False, "error": str(e)}
    else:
        return {"data": serializer.data, "success": True, "error": " "}


def delete_article(request, pk):
    try:
        article = Article.objects.get(pk=pk)
        article.is_active = False
        article.save()
    except District.DoesNotExist:
        return {"data": " ", "success": True, "error": "District Does Not Exist"}
    except Exception as e:
        return {"data": " ", "success": False, "error": str(e)}
    else:
        return {"data": " ", "success": True, "error": " "}

