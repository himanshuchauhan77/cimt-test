# from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .casecontroller import add_case,get_all_natureofmisconduct,get_all_sourceofcomplaint,\
    get_all_articles
    # add_evidence,get_all_cases,get_all_evidence,get_cases_by_district
# from . models import Evidence
#
#


class AddCase(APIView):
    def post(self,request):
        data = add_case(request)
        return Response(data)


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














# class GetAllCase(APIView):
#
#     def get(self,request):
#         data = get_all_cases()
#         return JsonResponse(data)
#


# class AddEvidence(APIView):
#
#     def post(self,request):
#         data = add_evidence(request)
#         # kwargs = dict(request.data)
#         # print(kwargs)
#         # case_no = request.POST.get('case_no')
#         # evidence = Evidence()
#         # evidence.evidence_name= request.POST.get('evidence_name')
#         # evidence.evidence_desc = request.POST.get('evidence_desc')
#         # evidence.evidence_image = request.FILES['evidence_image']
#         # case = Case.objects.get(pk=case_no)
#         # evidence.case_no = case
#         # evidence.save()
#         return JsonResponse(data)
#
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
