import datetime
from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.utils import timezone
User = get_user_model()


class NatureOfMisconduct(models.Model):
    type = models.CharField(max_length=200)
    description = models.TextField()

# ----------------------------------------------------


class SourceOfComplaint(models.Model):
    type = models.CharField(max_length=200)
    description = models.TextField()

# --------------------------------------------------------------------------


def current_year():
    return datetime.date.today().year


class CaseIdentity(models.Model):
    file_number = models.IntegerField()
    file_year = models.IntegerField(default=current_year)
    office = models.ForeignKey('accounts.Office', on_delete=models.CASCADE, related_name="office_cases", default="")
    nature_of_misconduct = models.ForeignKey(NatureOfMisconduct, on_delete=models.CASCADE, related_name='nature_of_misconduct_cases')
    source_of_complaint = models.ForeignKey(SourceOfComplaint, on_delete=models.CASCADE, related_name='source_of_complaint_cases')
    name_of_complainant = models.CharField(max_length=200)
    complainant_address = models.TextField()
    # attachments = models.FileField()


def case_identity_directory_path(instance):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'case_{0}/case_identity_attachments/'.format(instance.case_identity_case.case_id)


class CaseIdentityAttachment(models.Model):
    case_identity = models.ForeignKey(CaseIdentity,on_delete=models.CASCADE)
    attachment = models.FileField(upload_to=case_identity_directory_path)

# ------------------------------------------------------------------------------------


class ChargedOfficer(models.Model):
    """ Table for Charged Officer"""
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    previous_charges = models.TextField()


def charged_officer_directory_path(instance):
    """Function to return Charged officer attachements Directory"""
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'case_{0}/charged_officer_attachments/'.format(instance.charged_officer_cases.case_id)


class ChargedOfficerAttachment(models.Model):
    """Model for Attachments with Charged Officer Table"""
    charged_officer = models.ForeignKey(ChargedOfficer,on_delete=models.CASCADE)
    attachment = models.FileField(upload_to=charged_officer_directory_path)


# ------------------------------------------------------------------------------------


class Article(models.Model):
    """Article Table"""
    name = models.CharField(max_length=100)
    article_no = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class DraftArticle(models.Model):
    draft_article_no = models.ForeignKey(Article,on_delete=models.CASCADE)
    gist_of_article = models.TextField()
    date_of_misconduct = models.DateField()
    misconduct_type = models.ForeignKey(NatureOfMisconduct,on_delete=models.CASCADE)
    amount_involved_if_any = models.BigIntegerField


def draft_article_directory_path(instance):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'case_{0}/draft_article_attachments/'.format(instance.article_cases.case_id)


class DraftArticleAttachments(models.Model):
    draft_article = models.ForeignKey(DraftArticle,on_delete=models.CASCADE,related_name='enquiry_attachments')
    attachment = models.FileField(upload_to=draft_article_directory_path)


class PreliminaryEnquiry(models.Model):
    enquiry_officer = models.CharField(max_length=100)
    report_date = models.DateField(auto_now=True)
    office = models.ForeignKey('accounts.office',on_delete=models.CASCADE)
    designation = models.ForeignKey('accounts.designation',on_delete=models.CASCADE)
    report_conclusion_breif = models.TextField()
    follow_up_action = models.TextField()
    draft_article = models.ForeignKey(DraftArticle,related_name="preliminary_enquiries",on_delete=models.CASCADE,default='')


def draft_article_preliminary_enquiry_directory_path(instance):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'case_{0}/draft_article_attachments/preliminary_enquiry_attachments'.format(instance.draft_article.article_cases.case_id)


class PrelinminaryEnquiryAttachments(models.Model):
    premilinary_enquiry = models.ForeignKey(PreliminaryEnquiry,on_delete=models.CASCADE,related_name='enquiry_attachments')
    attachment = models.FileField(upload_to=draft_article_preliminary_enquiry_directory_path)


# ---------------------------------------------------------------------------------------------


class Case(models.Model):
    STATUS = [
        ('COMPLETE','Complete'),
        ('PENDING','Pending'),
    ]
    case_id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    # fir_no = models.IntegerField(unique=True)
    case_identity = models.OneToOneField(CaseIdentity,on_delete=models.CASCADE,related_name='case_identity_case')
    charged_officer = models.ManyToManyField(ChargedOfficer,related_name='charged_officer_cases')
    # draft_chargesheet_proposal = models.OneToOneField(DraftChargeSheetProposal,on_delete=models.CASCADE,related_name='chargesheet_case')
    draft_article = models.ManyToManyField(DraftArticle,related_name='article_cases')
    status = models.CharField(max_length=10,choices=STATUS)

    # def __str__(self):
    #     return self.status

# class Evidence(models.Model):
#
#     case_no = models.ForeignKey(Case,on_delete=models.CASCADE)
#     evidence_image = models.ImageField(upload_to=f'{case_directory_path}/evidences/')
#     evidence_name = models.CharField(max_length=100)
#     evidence_desc = models.CharField(max_length=200)
#
#     def __str__(self):
#         return self.evidence_name
#
#
# def draft_directory_path(instance):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     return 'case_{0}/draft_attachments/'.format(instance.draft_no.case)


# class DraftSheetAttachment(models.Model):
#     draft_no = models.ForeignKey(DraftChargeSheetProposal,on_delete=models.CASCADE)
#     case = models.ForeignKey(Case,on_delete=models.CASCADE)
#     attachment = models.FileField(upload_to=draft_directory_path)
#

# ------------------------------------------------------------------


class DraftChargeSheetProposal(models.Model):
    file_rc_no = models.BigIntegerField()
    date = models.DateField(default=timezone.now)
    submitted_by = models.ForeignKey('accounts.Office',on_delete=models.CASCADE,related_name="office_submitted_by")
    submitted_to = models.ForeignKey('accounts.Office',on_delete=models.CASCADE,related_name="officer_submitted_to")
    subject = models.TextField()
    case = models.ForeignKey(Case,on_delete=models.CASCADE,related_name='draft_charge_sheets')


def draft_directory_path(instance):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'case_{0}/draft_charge_sheet_attachments/'.format(instance.chargesheet_case.case_id)


class DraftSheetAttachment(models.Model):
    draft_no = models.ForeignKey(DraftChargeSheetProposal,on_delete=models.CASCADE)
    attachment = models.FileField(upload_to=draft_directory_path)


