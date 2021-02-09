from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import *
from django.contrib.auth import get_user_model
# from django.apps import apps
User = get_user_model()
from django.contrib.auth.admin import UserAdmin
#
class UserAdmin(UserAdmin):
    pass
#
admin.site.register(User,UserAdmin)
admin.site.register(District)
admin.site.register(Office)
admin.site.register(Designation)
