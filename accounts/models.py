from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from post_office import mail

# import django_rest_passwordreset.urls

from cimt import settings

Group.add_to_class('description', models.CharField(max_length=180,null=True, blank=True))


# class State(models.Model):
#     state = models.CharField(max_length=200)
#     is_active = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.state



# class Division(models.Model):
#     division = models.CharField(max_length=100)
#     is_active = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.division


class District(models.Model):
    district = models.CharField(max_length=300)
    is_active = models.BooleanField(default=True)
    # state = models.ForeignKey(State,on_delete=models.CASCADE,related_name="districts",default="")

    def __str__(self):
        return self.district


class Office(models.Model):
    office_name = models.CharField(max_length=200)
    office_address = models.TextField()
    is_active = models.BooleanField(default=True)
    district = models.ForeignKey(District,on_delete=models.CASCADE,related_name="offices",default="")
    # user = models.OneToOneField(User)

    def __str__(self):
        return self.office_name


class Designation(models.Model):
    designation = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.designation


class UserProfile(AbstractUser):
    email = models.EmailField(unique=True,blank=False,null=False)
    # alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    profile_pic = models.ImageField(upload_to='profile_pics/',null=True,blank=True)
    office = models.ForeignKey(Office,on_delete=models.CASCADE,null=True)
    treasury_code = models.CharField(max_length=200)
    designation = models.ForeignKey(Designation,on_delete=models.CASCADE,null=True)
    phone_no = models.CharField(max_length=17,validators=[phone_regex],default='')


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    mail.send(
        [reset_password_token.user.email, ],
        subject= "Password Reset for {title}".format(title="Some website title"),
        message=email_plaintext_message,
        priority='now',
    )


    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "",
        # to:
        [reset_password_token.user.email]
    )



# class PinCode(models.Model):
#     pincode = models.BigIntegerField()
#     is_active = models.BooleanField(default=True)


