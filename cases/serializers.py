from django.core.files.storage import Storage
from accounts.serializers import AddUserSerializer,GetUserSerializer
from .models import CaseIdentity, ChargedOfficer, DraftChargeSheetProposal, \
    DraftArticle, Case, NatureOfMisconduct, SourceOfComplaint, PreliminaryEnquiry, Article, Evidence
from accounts.serializers import OfficeSerializer
from rest_framework import serializers
from accounts.models import Office
from django.contrib.auth import get_user_model
User = get_user_model()
from django.conf import settings


# class CaseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Case
#         fields = '__all__'
#         exclude = ('created_date',)
#
class AddEvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = '__all__'


class NatureOfMisconductSerializer(serializers.ModelSerializer):
    class Meta:
        model = NatureOfMisconduct
        fields = '__all__'


class SourceOfComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceOfComplaint
        fields = '__all__'


class PreliminaryEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = PreliminaryEnquiry
        fields = '__all__'


class CaseIdentitySerializer(serializers.ModelSerializer):
    nature_of_misconduct = NatureOfMisconductSerializer
    source_of_complaint = SourceOfComplaintSerializer
    office = OfficeSerializer

    class Meta:
        model = CaseIdentity
        fields = '__all__'

    # def create(self, validated_data):
    #     nature_of_misconduct_data = validated_data.pop('nature_of_misconduct')
    #     source_of_complaint_data = validated_data.pop('source_of_complaint')
    #     office_data = validated_data.pop('office')
    #     case_identity = CaseIdentity.objects.create(**validated_data)
    #     return case_identity


class ChargedOfficerSerializer(serializers.ModelSerializer):
    user = GetUserSerializer()

    class Meta:
        model = ChargedOfficer
        fields = '__all__'


class DraftChargeSheetProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftChargeSheetProposal
        exclude = ('case',)


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class DraftArticleSerializer(serializers.ModelSerializer):
    preliminary_enquiries = PreliminaryEnquirySerializer(many=True)

    class Meta:
        model = DraftArticle
        fields = ('draft_article_no','gist_of_article','date_of_misconduct','misconduct_type','amount_involved_if_any','preliminary_enquiries')

    # def create(self, validated_data):
    #     prelim_enquiries = validated_data.pop('preliminary_enquiries')
    #     draft_article = DraftArticle.objects.create(**validated_data)
    #     preliminary_enquiries = []
    #     for enquiry in prelim_enquiries:
    #         prelim_enquiry = PreliminaryEnquiry.objects.create(**enquiry)
    #         preliminary_enquiries.append(prelim_enquiry)
    #     draft_article.preliminary_enquiries.add(*preliminary_enquiries)
    #     return draft_article


class CaseSerializer(serializers.ModelSerializer):
    case_identity = CaseIdentitySerializer(required=True)
    charged_officer = ChargedOfficerSerializer(many=True)
    draft_charge_sheets = DraftChargeSheetProposalSerializer(many=True)
    draft_article = DraftArticleSerializer(many=True)

    class Meta:
        model = Case
        # fields = '__all__'
        exclude = ('case_id',)

    def create(self, validated_data):

        case_identities_data = validated_data.pop('case_identity', [])
        charged_officers_data = validated_data.pop('charged_officer', [])
        draft_chargesheet_proposals_data = validated_data.pop('draft_charge_sheets', [])
        draft_articles_data = validated_data.pop('draft_article', [])
        case_identity = CaseIdentitySerializer.create(CaseIdentitySerializer(), validated_data=case_identities_data)
        # draft_chargesheet_proposal = DraftChargeSheetProposalSerializer.create(DraftChargeSheetProposalSerializer(),validated_data=draft_chargesheet_proposals_data)

        case = Case.objects.create(case_identity=case_identity,**validated_data)

        officers = []
        for charged_officer_data in charged_officers_data:
            # charged_officer_attachment_url = charged_officer_data.pop('attachment', None)
            charged_officer = ChargedOfficer.objects.create(**charged_officer_data)
            # attachment = ChargedOfficerAttachment.objects.create(charged_officer=charged_officer,attachment=charged_officer_attachment)
            officers.append(charged_officer)
        case.charged_officer.add(*officers)

        draft_chargesheet_proposals = []
        for draft_chargesheet_proposal_data in draft_chargesheet_proposals_data:
            # draft_chargesheet_proposal_attachments = draft_chargesheet_proposal_data.pop('attachments', None)
            draft_sheet = DraftChargeSheetProposal.objects.create(case=case,**draft_chargesheet_proposal_data)
            # for attachment_data in draft_chargesheet_proposal_attachments:
            #     attachment = DraftSheetAttachment.objects.create(draft_no=draft_sheet,attachment=attachment_data)
            # draft_chargesheet_proposals.append(draft_sheet)

        draft_articles = []
        for draft_article_data in draft_articles_data:
            # article_no = draft_article_data.pop('draft_article_no')
            # article = Article.objects.get(article_no=article_no)
            # draft_article_attachments = draft_article_data.pop('attachments')
            preliminary_enquiries_list = draft_article_data.pop('preliminary_enquiries')
            draft_article = DraftArticle.objects.create(**draft_article_data)
            # for draft_article_attachment in draft_article_attachments:
            #     draft_attachment = DraftArticleAttachments.objects.create()
            for enquiry in preliminary_enquiries_list:
                # preliminary_enquiry_attachments = enquiry.pop('attachments')
                preliminary_enquiry = PreliminaryEnquiry.objects.create(draft_article=draft_article,**enquiry)
                # for enquiry_attachment in preliminary_enquiry_attachments:
                #     preliminary_enquiry_attachment = PrelinminaryEnquiryAttachments.objects.create(premilinary_enquiry= preliminary_enquiry,attachment=enquiry_attachment)
            # draft_article.preliminary_enquiries.set(preliminary_enquiries_list
            draft_articles.append(draft_article)
            case.draft_article.add(*draft_articles)
        return case
