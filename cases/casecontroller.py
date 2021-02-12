from django.db.models import Count, F
import json
from django.db.models.functions import TruncMonth
import json
from .serializers import CaseSerializer
from .models import Case,NatureOfMisconduct,SourceOfComplaint,Article
# from accounts.models import District
from cases.matching import app


def add_case(request):
    """Case controller for adding case"""
    serializer = CaseSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return {"data": "case created", 'success': True, "error": ""}
    else:
        return {"data":"","success":False,"error":f"{serializer.errors}"}

    # case = Case.objects.create(**kwargs)
    # case.save()

# def json_dt_patch(o):
#     import datetime
#     if isinstance(o, datetime.date) or isinstance(o, datetime.datetime):
#         return o.strftime("%Y/%m/%d %H:%M:%S")
#     return o


def get_case_detail(request,case_id):
    case = Case.objects.get(case_id=case_id)
    serializer = CaseSerializer(case)
    j = json.dumps(serializer.data,default= str)
    return j
    # print(serializer.data)



def get_all_natureofmisconduct(request):
    try:
        data = list(NatureOfMisconduct.objects.all().order_by('id').values())
    except Exception as e:
        print(str(e))
        return {"data": " ", "success": False, "error": str(e)}
    return {"data": data, "success": True, "error": " "}


def get_all_sourceofcomplaint(request):
    try:
        data = list(SourceOfComplaint.objects.all().order_by('type').values())
    except Exception as e:
        print(str(e))
        return {"data": " ", "success": False, "error": str(e)}
    return {"data": data, "success": True, "error": " "}


def get_all_articles(request):
    try:
        data = list(Article.objects.all().order_by('article_no').values())
    except Exception as e:
        print(str(e))
        return {"data": " ", "success": False, "error": str(e)}
    return {"data": data, "success": True, "error": " "}


def get_cases_report(request):
    total_cases = Case.objects.count()
    ongoing_cases = Case.objects.filter(status="ONGOING").count()
    complete_cases = Case.objects.filter(status="COMPLETE").count()
    return {'total_cases':total_cases,'ongoing_cases':ongoing_cases,'complete_cases':complete_cases}


def get_monthly_case_report(request):

    total_cases = Case.objects.annotate(month = TruncMonth('created_date')).values('month')\
        .annotate(c = Count('case_id')).values('month','c')

    ongoing_cases = Case.objects.filter(status='ONGOING')\
        .annotate(month = TruncMonth('created_date')).values('month').annotate(c = Count('status')).values('month','c')

    complete_cases = Case.objects.filter(status='COMPLETE').annotate(month = TruncMonth('created_date')).values('month').annotate(c = Count('status')).values('month','c')

    return {'total_monthly_cases':total_cases,'ongoing_monthly_cases':ongoing_cases,'complete_monthly_cases':complete_cases}


def get_district_cases_report(request):
    total_cases = Case.objects.annotate(district=F('case_identity__office__office_name')).annotate(c=Count('case_id')).count()
    dist_cases = Case.objects.annotate(district = F('case_identity__office__office_name')).values('district')\
        .annotate(c = Count('case_id')).values('district','c')

    dist_list = {}
    for case in dist_cases:
        dist_list['district'] = case['district']
        dist_list['percentage'] = case['c']/total_cases*100

    return {'data':dist_list,'success':True,'error':''}












# def get_all_cases():
#     """Returns List of all Cases"""
#     try:
#         success = True
#         error = " "
#         all_roles = Case.objects.all().order_by("case_no").values()
#         data = list(all_roles)
#     except Exception as e:
#         error = str(e)
#         success = False
#         data = " "
#     return {"data": data, "success": success, "error": error}


def add_evidence(request):
    """Adding Evidence"""
    serializer = AddEvidenceSerializer(data= request.data)
    if serializer.is_valid():
        # evidenceimg = request.FILES['evidence_image']
        # fs = FileSystemStorage()
        # filename = fs.save(evidenceimg.name,evidenceimg)
        # uploaded_file_url = fs.url(filename)
        print(serializer.validated_data)
        obj = serializer.save()
        uploaded_file_url = f"localhost:8000:{obj.evidence_image.url}"
        # print(obj.evidence_image.name)
        # print(obj.evidence_image)
        # print(uploaded_file_url)
        # path1 = os.path.abspath(f"{uploaded_file_url}")
        # print(path1)
        # urllib.request.urlretrieve(uploaded_file_url,f"/home/himanshu/djangofull/Workspace/cimt/cases/matching/evidence/")
        match_status = app.main(f"{obj.evidence_image}")
        return { "uploaded_file_url": uploaded_file_url,"match_status": match_status}
    else:
        return {"data":"","success":False,"error":f"{serializer.errors}"}


# def get_all_evidence(request,case_no):
#     """Returns all Evidence of according to a case"""
#     all_evidence = Evidence.objects.filter(case_no = case_no)
#     data = list(all_evidence.values())
#     url = []
#     for item in all_evidence:
#         url.append(item.evidence_image.url)
#     # print(url)
#     for i in range(len(data)):
#         data[i]['url'] = url[i]
#     return data


# def get_cases_by_district(request,id):
#     """Returns Cases in one district"""
#     dist = District.objects.get(pk=id)
#     cases = dist.district_cases.all().order_by("case_no").values()
#     data = list(cases)
#     return {"data": data, "success": True, "error": ""}
