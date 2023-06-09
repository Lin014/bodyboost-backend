from rest_framework import serializers
from .models import *


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

class FoodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodType
        fields = '__all__'

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'

class CustomFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomFood
        fields = '__all__'

class DietRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietRecord
        fields = '__all__'

class DailyBonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyBonus
        fields = '__all__'
