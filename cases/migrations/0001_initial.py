# Generated by Django 3.1.4 on 2021-03-10 06:21

import cases.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('article_no', models.IntegerField(unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('case_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('COMPLETE', 'Complete'), ('ONGOING', 'Ongoing')], default='ONGOING', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='DraftArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gist_of_article', models.TextField()),
                ('date_of_misconduct', models.DateField()),
                ('draft_article_attachment', models.CharField(max_length=200)),
                ('draft_article_attachment_desc', models.TextField()),
                ('draft_article_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.article')),
            ],
        ),
        migrations.CreateModel(
            name='NatureOfMisconduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SourceOfComplaint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PreliminaryEnquiry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enquiry_officer', models.CharField(max_length=100)),
                ('report_date', models.DateField(auto_now=True)),
                ('report_conclusion_breif', models.TextField()),
                ('follow_up_action', models.TextField()),
                ('preliminary_enquiry_attachment', models.CharField(max_length=200)),
                ('preliminary_enquiry_attachment_desc', models.TextField()),
                ('designation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.designation')),
                ('draft_article', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='preliminary_enquiries', to='cases.draftarticle')),
                ('office', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.office')),
            ],
        ),
        migrations.CreateModel(
            name='Evidence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evidence_image', models.ImageField(upload_to=cases.models.case_directory_path)),
                ('evidence_name', models.CharField(max_length=100)),
                ('evidence_desc', models.CharField(max_length=200)),
                ('case_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.case')),
            ],
        ),
        migrations.CreateModel(
            name='DraftChargeSheetProposal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_rc_no', models.BigIntegerField()),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('subject', models.TextField()),
                ('draft_charge_sheet_proposal_attachments', models.CharField(max_length=200)),
                ('draft_charge_sheet_attachment_desc', models.TextField(blank=True, null=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='draft_charge_sheets', to='cases.case')),
                ('submitted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='office_submitted_by', to='accounts.office')),
                ('submitted_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='officer_submitted_to', to='accounts.office')),
            ],
        ),
        migrations.AddField(
            model_name='draftarticle',
            name='misconduct_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.natureofmisconduct'),
        ),
        migrations.CreateModel(
            name='ChargedOfficer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('previous_charges', models.TextField()),
                ('charged_officer_attachment', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CaseIdentity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_number', models.IntegerField()),
                ('file_year', models.DateField(auto_now=True)),
                ('name_of_complainant', models.CharField(max_length=200)),
                ('complainant_address', models.TextField()),
                ('case_identity_attachment', models.CharField(max_length=200)),
                ('case_identity_attachment_desc', models.TextField(blank=True, null=True)),
                ('nature_of_misconduct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nature_of_misconduct_cases', to='cases.natureofmisconduct')),
                ('office', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='office_cases', to='accounts.office')),
                ('source_of_complaint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_of_complaint_cases', to='cases.sourceofcomplaint')),
            ],
        ),
        migrations.AddField(
            model_name='case',
            name='case_identity',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='case_identity_case', to='cases.caseidentity'),
        ),
        migrations.AddField(
            model_name='case',
            name='charged_officer',
            field=models.ManyToManyField(related_name='charged_officer_cases', to='cases.ChargedOfficer'),
        ),
        migrations.AddField(
            model_name='case',
            name='draft_article',
            field=models.ManyToManyField(related_name='article_cases', to='cases.DraftArticle'),
        ),
    ]
