from rest_framework import serializers
from .models import *


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = profile
        fields = '__all__'

class EmailVerifyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerifyCode
        fields = '__all__'