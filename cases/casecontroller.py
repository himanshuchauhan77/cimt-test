from django.db.models import Count, F
import json
from django.db.models.functions import TruncMonth
import json

from . import serializers
from .serializers import CaseSerializer, AddEvidenceSerializer, ChargedOfficerSerializer
from .models import Case, NatureOfMisconduct, SourceOfComplaint, Article, Evidence
# from accounts.models import District
from cases.matching import app


def add_case(request):
    """Case controller for adding case"""
    serializer = CaseSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return {"data": "case created", 'success': True, "error": ""}
    else:
        return {"data": "", "success": False, "error": f"{serializer.errors}"}

    # case = Case.objects.create(**kwargs)
    # case.save()


# def json_dt_patch(o):
#     import datetime
#     if isinstance(o, datetime.date) or isinstance(o, datetime.datetime):
#         return o.strftime("%Y/%m/%d %H:%M:%S")
#     return o


def get_case_detail(request, case_id):
    case = Case.objects.get(case_id=case_id)
    try:
        serializer = CaseSerializer(case)
        all_evidence = Evidence.objects.filter(case_no=case_id)
        evidence_ser = AddEvidenceSerializer(all_evidence,many=True)
        new_dict = {}
        new_dict.update(serializer.data)
        new_dict['evidences']=evidence_ser.data
    except Exception as e:
        new_dict2 = {"data": "", "success": True, "error": f"{str(e)}"}
        return json.dumps(new_dict2, default=str)
    new_dict2 = {"data":new_dict,"success":True,"error":""}
    j = json.dumps(new_dict2, default=str)
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

# ---------------------- Dashboard -------------------


def get_cases_report(request):
    total_cases = Case.objects.count()
    ongoing_cases = Case.objects.filter(status="ONGOING").count()
    complete_cases = Case.objects.filter(status="COMPLETE").count()
    return {'total_cases': total_cases, 'ongoing_cases': ongoing_cases, 'complete_cases': complete_cases}


def get_monthly_case_report(request):
    total_cases = Case.objects.annotate(month=TruncMonth('created_date')).values('month') \
        .annotate(c=Count('case_id')).values('month', 'c')

    ongoing_cases = Case.objects.filter(status='ONGOING') \
        .annotate(month=TruncMonth('created_date')).values('month').annotate(c=Count('status')).values('month', 'c')

    complete_cases = Case.objects.filter(status='COMPLETE').annotate(month=TruncMonth('created_date')).values(
        'month').annotate(c=Count('status')).values('month', 'c')

    return {'total_monthly_cases': total_cases, 'ongoing_monthly_cases': ongoing_cases,
            'complete_monthly_cases': complete_cases}


def get_district_cases_report(request):
    total_cases = Case.objects.annotate(district=F('case_identity__office__office_name')).annotate(
        c=Count('case_id')).count()
    dist_cases = Case.objects.annotate(district=F('case_identity__office__office_name')).values('district') \
        .annotate(c=Count('case_id')).values('district', 'c')

    dist_list = {}
    for case in dist_cases:
        dist_list['district'] = case['district']
        dist_list['percentage'] = case['c'] / total_cases * 100

    return {'data': dist_list, 'success': True, 'error': ''}


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
    serializer = AddEvidenceSerializer(data=request.data)
    try:
        if serializer.is_valid(raise_exception=True):
            # evidenceimg = request.FILES['evidence_image']
            # fs = FileSystemStorage()
            # filename = fs.save(evidenceimg.name,evidenceimg)
            # uploaded_file_url = fs.url(filename)
            # print(serializer.validated_data)
            obj = serializer.save()
            uploaded_file_url = obj.evidence_image.url
            # print(obj.evidence_image.name)
            # print(obj.evidence_image)
            # print(uploaded_file_url)
            # path1 = os.path.abspath(f"{uploaded_file_url}")
            # print(path1)
            # urllib.request.urlretrieve(uploaded_file_url,f"/home/himanshu/djangofull/Workspace/cimt/cases/matching/evidence/")
            match_status,img2,x,y = app.main(f"{obj.evidence_image}")
            if match_status:
                obj.matched_image = img2
                obj.match_status = match_status
                obj.save()
                return {"data": {"uploaded_file_url": f"{uploaded_file_url}", "match_status": f"{match_status}","matched_image":f"{img2}",\
                                 "keypoints_fig":f"{x}","matching_fig":f"{y}"},
                        "success": True, "error": ""}
            else:
                return {"data": {"uploaded_file_url": "", "match_status": f"{match_status}"},"success": True, "error": ""}
    except Exception as e:
        return {"data": "", "success": False, "error": str(e)}


def get_all_evidence(request,case_no):
    """Returns all Evidence of according to a case"""
    all_evidence = Evidence.objects.filter(case_no = case_no)
    data = list(all_evidence.values())
    url = []
    for item in all_evidence:
        url.append(item.evidence_image.url)
    # print(url)
    for i in range(len(data)):
        data[i]['url'] = url[i]
    return data


# def get_cases_by_district(request,id):
#     """Returns Cases in one district"""
#     dist = District.objects.get(pk=id)
#     cases = dist.district_cases.all().order_by("case_no").values()
#     data = list(cases)
#     return {"data": data, "success": True, "error": ""}


def get_all_charged_officer(request):
    case_id = request.data.get('case_id')
    print(case_id)
    charge_sheet = Case.objects.get(case_id=case_id)
    all_charged_officers = charge_sheet.charged_officer.all()
    serializer = ChargedOfficerSerializer(all_charged_officers,many=True)
    return {"charged_officers":serializer.data,"success":True,"error":""}

# ----------------------- Nature Of Misconduct -------------------------------------


def add_misconduct_type(request):
    # data = JSONParser().parse(request)
    serializer = serializers.NatureOfMisconductSerializer(data=request.data)
    try:
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    except Exception as e:
        return {"data": " ", "success": False, "error": str(e)}
    return {"data": serializer.data, "success": True, "error": " "}


def get_all_misconduct_type(request):
    try:
        data = list(NatureOfMisconduct.objects.all().order_by('id').values())
    except Exception as e:
        print(str(e))
        return {"data": " ", "success": False, "error": str(e)}
    return {"data": data, "success": True, "error": " "}


def get_misconduct_type(request,pk):
    try:
        nature_of_misconduct = NatureOfMisconduct.objects.get(pk=pk)
        serializer = serializers.NatureOfMisconductSerializer(nature_of_misconduct)
    except NatureOfMisconduct.DoesNotExist:
        return {"data": " ", "success": True, "error": "Office Does Not Exist"}
    except Exception as e:
        return {"data":" ","success":True,"error":str(e)}
    else:
        return {"data":serializer.data,"success":True,"error":" "}


def update_misconduct_type(request, pk):
    try:
        nature_of_misconduct = NatureOfMisconduct.objects.get(pk=pk)
        # data = JSONParser().parse(request)
        serializer = serializers.NatureOfMisconductSerializer(nature_of_misconduct, data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    except NatureOfMisconduct.DoesNotExist:
        return {"data": " ", "success": True, "error": "Office Does Not Exist"}
    except Exception as e:
        return {"data": " ", "success": False, "error": str(e)}
    else:
        return {"data": serializer.data, "success": True, "error": " "}


def delete_misconduct_type(request, pk):
    try:
        nature_of_misconduct = NatureOfMisconduct.objects.get(pk=pk)
        nature_of_misconduct.delete()
    except NatureOfMisconduct.DoesNotExist:
        return {"data": " ", "success": True, "error": "Office Does Not Exist"}
    except Exception as e:
        return {"data": " ", "success": False, "error": str(e)}
    else:
        return {"data": "Misconduct Type Deleted Successfully ", "success": True, "error": " "}


# ----------------------- Chargesheet --------------------

def get_all_chargesheet(request):
    try:
        cases = Case.objects.all().order_by('case_id')
        print(cases)
        serializer = CaseSerializer(cases,many=True)
    except Exception as e:
        print(str(e))
        return json.dumps({"data": " ", "success": False, "error": str(e)})
    return json.dumps({ "data": serializer.data,"success":True,"error":"" }, default=str)


# --------------------------Articles ---------------------------------


def add_article(request):
    # data = JSONParser().parse(request)
    serializer = serializers.ArticleSerializer(data=request.data)
    try:
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    except Exception as e:
        return {"data": " ", "success": False, "error": str(e)}
    return {"data": serializer.data, "success": True, "error": " "}


def get_all_articles(request):
    try:
        all_articles = Article.objects.all()
        serializer = serializers.ArticleSerializer(all_articles,many=True)
    except Exception as e:
        print(str(e))
        return {"data": " ", "success": False, "error": str(e)}
    return {"data": serializer.data, "success": True, "error": " "}


def get_article(request,pk):
    try:
        article = Article.objects.get(pk=pk)
        serializer = serializers.ArticleSerializer(article)
    except NatureOfMisconduct.DoesNotExist:
        return {"data": " ", "success": True, "error": "Office Does Not Exist"}
    except Exception as e:
        return {"data":" ","success":True,"error":str(e)}
    else:
        return {"data":serializer.data,"success":True,"error":" "}


def update_article(request, pk):
    try:
        article = Article.objects.get(pk=pk)
        # data = JSONParser().parse(request)
        serializer = serializers.ArticleSerializer(article, data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    except Article.DoesNotExist:
        return {"data": " ", "success": True, "error": "Office Does Not Exist"}
    except Exception as e:
        return {"data": " ", "success": False, "error": str(e)}
    else:
        return {"data": serializer.data, "success": True, "error": " "}


def delete_article(request, pk):
    try:
        article = Article.objects.get(pk=pk)
        article.delete()
    except Article.DoesNotExist:
        return {"data": " ", "success": True, "error": "Office Does Not Exist"}
    except Exception as e:
        return {"data": " ", "success": False, "error": str(e)}
    else:
        return {"data": "Misconduct Type Deleted Successfully ", "success": True, "error": " "}

