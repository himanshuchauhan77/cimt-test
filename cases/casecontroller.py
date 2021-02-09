from .serializers import CaseSerializer
from .models import Case,NatureOfMisconduct,SourceOfComplaint,Article
# from accounts.models import District
# from cases.matching import app


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


# def add_evidence(request):
#     """Adding Evidence"""
#     serializer = AddEvidenceSerializer(data= request.data)
#     if serializer.is_valid():
#         # evidenceimg = request.FILES['evidence_image']
#         # fs = FileSystemStorage()
#         # filename = fs.save(evidenceimg.name,evidenceimg)
#         # uploaded_file_url = fs.url(filename)
#         print(serializer.validated_data)
#         obj = serializer.save()
#         uploaded_file_url = f"localhost:8000:{obj.evidence_image.url}"
#         # print(obj.evidence_image.name)
#         # print(obj.evidence_image)
#         # print(uploaded_file_url)
#         # path1 = os.path.abspath(f"{uploaded_file_url}")
#         # print(path1)
#         # urllib.request.urlretrieve(uploaded_file_url,f"/home/himanshu/djangofull/Workspace/cimt/cases/matching/evidence/")
#         match_status = app.main(f"{obj.evidence_image}")
#         return { "uploaded_file_url": uploaded_file_url,"match_status": match_status}
#     else:
#         return {"data":"","success":False,"error":f"{serializer.errors}"}


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

