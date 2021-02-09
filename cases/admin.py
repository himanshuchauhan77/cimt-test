from django.apps import apps
from django.contrib import admin
from .models import *

admin.site.register(NatureOfMisconduct)
admin.site.register(SourceOfComplaint)
admin.site.register(CaseIdentity)
admin.site.register(ChargedOfficer)
admin.site.register(DraftChargeSheetProposal)
admin.site.register(PreliminaryEnquiry)
admin.site.register(Article)
admin.site.register(DraftArticle)
admin.site.register(Case)
