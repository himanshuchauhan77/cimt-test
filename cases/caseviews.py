# from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .casecontroller import add_case, get_all_natureofmisconduct, get_all_sourceofcomplaint, \
    get_all_articles, get_case_detail, add_evidence, get_all_charged_officer, get_all_chargesheet
from cases.casecontroller import get_cases_report, get_monthly_case_report, get_district_cases_report
from cases import casecontroller
# add_evidence,get_all_cases,get_all_evidence,get_cases_by_district
# from . models import Evidence


class AddCase(APIView):
    def post(self,request):
        data = add_case(request)
        return Response(data)


class GetCaseDetail(APIView):
    def get(self,request,case_id):
        data = get_case_detail(request,case_id)
        return HttpResponse(data,content_type='application/json')


class GetAllNatureOfMisconduct(APIView):
    def get(self,request):
        response = get_all_natureofmisconduct(request)
        return Response(response)


class GetSourceOfComplaint(APIView):
    def get(self,request):
        response = get_all_sourceofcomplaint(request)
        return Response(response)


class GetAllArticles(APIView):
    def get(self, request):
        response = get_all_articles(request)
        return Response(response)


# ----------------- DashBoard-----------------


class GetCaseReport(APIView):

    def get(self,request):
        data = get_cases_report(request)
        return Response(data)


class GetMonthlyCaseReport(APIView):

    def get(self,request):
        data = get_monthly_case_report(request)
        return Response(data)


class GetDistrictReport(APIView):
    def get(self,request):
        data = get_district_cases_report(request)
        return Response(data)






# class GetAllCase(APIView):
#
#     def get(self,request):
#         data = get_all_cases()
#         return JsonResponse(data)
#


class AddEvidence(APIView):

    def post(self,request):
        data = add_evidence(request)
        # kwargs = dict(request.data)
        # print(kwargs)
        # case_no = request.POST.get('case_no')
        # evidence = Evidence()
        # evidence.evidence_name= request.POST.get('evidence_name')
        # evidence.evidence_desc = request.POST.get('evidence_desc')
        # evidence.evidence_image = request.FILES['evidence_image']
        # case = Case.objects.get(pk=case_no)
        # evidence.case_no = case
        # evidence.save()
        return Response(data)

#
# class GetAllEvidence(APIView):
#
#     def get(self,request,case_no):
#         try:
#             data = get_all_evidence(request,case_no)
#             return JsonResponse({'data': data,"success":True,"error":""})
#         except Exception as e:
#             error = str(e)
#             return JsonResponse({'data': "", "success":True,"error":error})
#
#
#
#     # def get(self,id):
#     #     data = Evidence.objects.get(id = id)
#     #     url_evidence = data.evidence_image.url


# class GetCaseByDistrict(APIView):
#
#     def get(self,request,id):
#         data = get_cases_by_district(request,id)
#         return JsonResponse(data)


class UploadAttachment(APIView):
    def post(self,request):
        image = request.FILES.get('image')
        try:
            if image:
                fs = FileSystemStorage()
                file = fs.save(f'case_attachmets_/{image.name}', image)
                fileurl = fs.url(file)
            return Response({"data":f"{fileurl}","success":True,"error":""})
        except Exception as e:
            return Response({"data": "","success":True,"error":f"{str(e)}"})


class GetAllChargedOfficer(APIView):

    def post(self,request):
        data = get_all_charged_officer(request)
        return Response(data)


# -------------------- CRUD for MISCONDUCT ------------------

class MisconductTypeLIST(APIView):

    def post(self, request):
        data = casecontroller.add_misconduct_type(request)
        return Response(data)

    def get(self, request):
        data = casecontroller.get_all_misconduct_type(request)
        return Response(data)


class MisconductTypeDetail(APIView):

    def put(self, request, pk):
        data = casecontroller.update_misconduct_type(request, pk)
        return Response(data)

    def delete(self, request, pk):
        data = casecontroller.delete_misconduct_type(request, pk)
        return Response(data)

    def get(self,request,pk):
        data = casecontroller.get_misconduct_type(request,pk)
        return Response(data)


# --------------------------------------------------

class GetAllChargeSheet(APIView):

    def get(self,request):
        data = get_all_chargesheet(request)
        return HttpResponse(data,content_type='application/json')