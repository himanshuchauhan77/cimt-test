# Generated by Django 3.1.4 on 2021-03-11 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone_no',
            field=models.CharField(default='', max_length=17),
        ),
    ]
