from django.urls import path
from django.conf import settings
from .caseviews import AddCase, GetAllArticles, GetAllNatureOfMisconduct, GetSourceOfComplaint, GetCaseReport, \
    GetDistrictReport, GetMonthlyCaseReport, GetCaseDetail, AddEvidence,UploadAttachment
from django.conf.urls.static import static

urlpatterns = [
    path('addChargeSheet/',AddCase.as_view()),
    path('getCaseById/<int:case_id>/',GetCaseDetail.as_view()),


    path('natureMisconduct/',GetAllNatureOfMisconduct.as_view()),
    path('getAllArticles/',GetAllArticles.as_view()),
    path('sourceComplaint/',GetSourceOfComplaint.as_view()),
    # path('GetAllCase/',GetAllCase.as_view()),
    path('addEvidence/',AddEvidence.as_view()),

    # path('GetAllEvidence/<case_no>/',GetAllEvidence.as_view()),
    # path('GetCaseByDistrict/<int:id>/',GetCaseByDistrict.as_view()),
    path('uploadAttachment/',UploadAttachment.as_view()),

    path('getCaseReport/',GetCaseReport.as_view()),
    path('getMonthlyCaseReport/',GetMonthlyCaseReport.as_view()),
    path('getDistrictReport/',GetDistrictReport.as_view())

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)