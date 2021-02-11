from rest_framework import serializers
from . import models
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email','treasury_code','designation','profile_pic','phone_no','office']


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        """
        Validates user data.
        """
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        return data


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class CustomTokenSerializer(serializers.Serializer):
    token = serializers.CharField()




class AddRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name','description']
        extra_kwargs = {'name':{'required':True}}


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Office
        fields = ['office_name','office_address','district']


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Designation
        fields = '__all__'


# class DivisionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Division
#         fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.District
        fields = '__all__'


# class ArticleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Article
#         fields = 'all'

