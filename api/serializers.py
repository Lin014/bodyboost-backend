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

class AnimationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animation
        fields = '__all__'

class AccuracySerializer(serializers.ModelSerializer):
    class Meta:
        model = Accuracy
        fields = '__all__'

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class WeightHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeigthtHistory
        fields = '__all__'

class NotificationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationHistory
        fields = '__all__'

class BodyFatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyFatHistory
        fields = '__all__'

class WaterHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterHistory
        fields = '__all__'

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'

class UserAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAchievement
        fields = '__all__'

class GoalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalHistory
        fields = '__all__'

class AchievementRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AchievementRecord
        fields = '__all__'

class DietDayRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietDayRecord
        fields = '__all__'

class UserAchievedSportSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAchievedSport
        fields = '__all__'