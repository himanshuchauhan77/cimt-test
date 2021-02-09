from django.urls import path
from django.conf import settings
from .caseviews import AddCase,GetAllArticles,GetAllNatureOfMisconduct,GetSourceOfComplaint
from django.conf.urls.static import static

urlpatterns = [
    path('AddCase/',AddCase.as_view()),
    path('natureMisconduct/',GetAllNatureOfMisconduct.as_view()),
    path('getAllArticles/',GetAllArticles.as_view()),
    path('sourceComplaint/',GetSourceOfComplaint.as_view())
    # path('GetAllCase/',GetAllCase.as_view()),
    # path('AddEvidence/',AddEvidence.as_view()),
    # path('GetAllEvidence/<case_no>/',GetAllEvidence.as_view()),
    # path('GetCaseByDistrict/<int:id>/',GetCaseByDistrict.as_view()),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)