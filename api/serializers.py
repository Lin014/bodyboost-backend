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

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = '__all__'

class SportFrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = SportFrequency
        fields = '__all__'

class SportGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportGroup
        fields = '__all__'

class SportGroupItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportGroupItem
        fields = '__all__'

class SportRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportRecord
        fields = '__all__'

class SportRecordItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportRecordItem
        fields = '__all__'

class AnimatedCharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimatedCharacter
        fields = '__all__'

class AccuracySerializer(serializers.ModelSerializer):
    class Meta:
        model = Accuracy
        fields = '__all__'

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = '__all__'


    