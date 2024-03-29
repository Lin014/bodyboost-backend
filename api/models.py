from django.db import models
from django.utils import timezone

# done
class Users(models.Model):
    status_choices = [ 
        ('success', 'Success'), 
        ('verified', 'Verified'), 
        ('unverified', 'Unverified') 
    ]
    created_type_choices = [ 
        ('normal', 'Normal'),
        ('google', 'Google') 
    ]

    account = models.CharField(max_length=30)
    password = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField()
    created_type = models.CharField(max_length=20, choices=created_type_choices)
    status = models.CharField(max_length=20, choices=status_choices)
    created_at = models.DateTimeField(auto_now_add=True)

#done
class Member(models.Model):
    member_type_choices = [ 
        ('normal', 'Normal'),
        ('premium', 'Premium') 
    ]
    payment_type_choices = [
        ('month', '月繳'),
        ('year', '年繳')
    ]

    member_type = models.CharField(max_length=10, default='normal', choices=member_type_choices)
    phone = models.CharField(max_length=10, blank=True, null=True)
    is_trial = models.BooleanField(default=False)
    payment_type = models.CharField(max_length=15, blank=True, null=True)
    user_id = models.OneToOneField(Users, on_delete=models.CASCADE)


#done
class GoalHistory(models.Model):
    goal_choices = [
        ('health', '維持身體健康'),
        ('weight', '減重'),
        ('fat', '減脂'),
        ('muscle', '增肌'),
    ]

    goal = models.CharField(default='health', max_length=30, choices=goal_choices)
    start_date = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

# done
class Profile(models.Model):
    gender_choices = [(1, 1), (2, 2)]
    goal_choices = [
        ('health', '維持身體健康'),
        ('weight', '減重'),
        ('fat', '減脂'),
        ('muscle', '增肌'),
    ]

    name = models.CharField(max_length=50)
    gender = models.IntegerField(choices=gender_choices)
    birthday = models.DateField()
    height = models.FloatField()
    weight = models.FloatField()
    # 目標體重
    weight_goal = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='profile_img', default='')
    # 目標
    goal_id = models.ForeignKey(GoalHistory, on_delete=models.DO_NOTHING)
    # 體脂率
    body_fat = models.FloatField(blank=True, null=True)
    user = models.OneToOneField(Users, on_delete=models.CASCADE)

# done
class EmailVerifyCode(models.Model):
    send_type_choices = (
        ('register', '註冊'),
        ('forget', '忘記密碼')
    )
    code = models.CharField(max_length=15)
    email = models.EmailField()
    send_type = models.CharField(max_length=20, choices=send_type_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

# done
class DailyBonus(models.Model):
    date = models.DateTimeField(default=timezone.now)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

# done
class Store(models.Model):
    name = models.TextField(unique=True)

# done
class FoodType(models.Model):
    type = models.TextField(unique=True)

# done
# page
class Food(models.Model):
    name = models.TextField()
    calorie = models.FloatField()
    size = models.FloatField()
    unit = models.CharField(max_length=30)
    protein = models.FloatField()
    fat = models.FloatField()
    carb = models.FloatField()
    sodium = models.FloatField()
    modify = models.BooleanField()
    food_type_id = models.ForeignKey(FoodType, on_delete=models.SET(''))
    store_id = models.ForeignKey(Store, on_delete=models.SET(''))

# done
# page
class CustomFood(models.Model):
    name = models.TextField()
    calorie = models.FloatField()
    size = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=30, blank=True, null=True)
    protein = models.FloatField(blank=True, null=True)
    fat = models.FloatField(blank=True, null=True)
    carb = models.FloatField(blank=True, null=True)
    sodium = models.FloatField(blank=True, null=True)
    modify = models.BooleanField()
    food_type_id = models.ForeignKey(FoodType, on_delete=models.SET(''))
    store_id = models.ForeignKey(Store, on_delete=models.SET(''))
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

# done
class DietRecord(models.Model):
    date = models.DateTimeField()
    label = models.TextField(blank=True, null=True)
    serving_amount = models.FloatField()
    name = models.TextField()
    calorie = models.FloatField()
    size = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=30, blank=True, null=True)
    protein = models.FloatField(blank=True, null=True)
    fat = models.FloatField(blank=True, null=True)
    carb = models.FloatField(blank=True, null=True)
    sodium = models.FloatField(blank=True, null=True)
    modify = models.BooleanField(blank=True, null=True) #
    food_type_id = models.ForeignKey(FoodType, on_delete=models.SET(''))
    store_id = models.ForeignKey(Store, on_delete=models.SET(''))
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

# done
# page
class Sport(models.Model):
    type_choices = (
        ('aerobics', '有氧'),
        ('anaerobic', '無氧')
    )
    name = models.TextField(unique=True)
    description = models.TextField(blank=True, null=True)
    default_time = models.FloatField()
    interval = models.FloatField()
    is_count = models.BooleanField()
    met = models.FloatField()
    type = models.CharField(max_length=10, choices=type_choices)

# done
# page
class SportFrequency(models.Model):
    frequency = models.IntegerField()
    sport = models.OneToOneField(Sport, on_delete=models.CASCADE)

# done
# page
class SportGroup(models.Model):
    name = models.TextField()
    rest_time = models.FloatField()
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

# done
class SportGroupItem(models.Model):
    mode_choices = (
        ('timing', '計時'),
        ('counting', '計次'),
        ('none', '無限制')
    )

    no = models.IntegerField()
    mode = models.CharField(max_length=20, choices=mode_choices)
    custom_time = models.FloatField(blank=True, null=True)
    custom_counts = models.IntegerField(blank=True, null=True)
    sport_id = models.ForeignKey(Sport, on_delete=models.CASCADE)
    sport_group_id = models.ForeignKey(SportGroup, on_delete=models.CASCADE)

# done
# page
class SportRecord(models.Model):
    type_choices = (
        ('single', '單一運動'),
        ('combo', '組合運動')
    )

    rest_time = models.FloatField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=type_choices)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    total_time = models.FloatField(default=0)
    total_consumed_kcal = models.FloatField(default=0)
    cur_sport_no = models.IntegerField(default=0)
    is_record_video = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    sport_group_id = models.ForeignKey(SportGroup, on_delete=models.SET_NULL, blank=True, null=True)

# done
class SportRecordItem(models.Model):
    mode_choices = (
        ('timing', '計時'),
        ('counting', '計次'),
        ('none', '無限制')
    )

    completed_time = models.DateTimeField(blank=True, null=True)
    # copy sport field
    sport_id = models.ForeignKey(Sport, on_delete=models.DO_NOTHING)
    custom_time = models.FloatField(blank=True, null=True)
    custom_counts = models.IntegerField(blank=True, null=True)
    # other field
    no = models.IntegerField()
    mode = models.CharField(max_length=20, choices=mode_choices)
    time = models.FloatField(default=0)
    counts = models.IntegerField(default=0)
    consumed_kcal = models.FloatField(default=0)
    sport_record_id = models.ForeignKey(SportRecord, on_delete=models.CASCADE)
    video = models.FileField(upload_to='record_video', blank=True, null=True)

# done
class Animation(models.Model):
    name = models.CharField(max_length=15)
    animation = models.FileField(upload_to='animation_video', blank=True, null=True)
    image = models.ImageField(upload_to='animation_img', blank=True, null=True)
    sport_id = models.ForeignKey(Sport, on_delete=models.CASCADE)

# modify
class Accuracy(models.Model):
    accuracy = models.FloatField()
    label = models.CharField(max_length=15)
    sport_record_item_id = models.ForeignKey(SportRecordItem, on_delete=models.CASCADE)

# done
class Setting(models.Model):
    theme_choices = (
        ('light', '日間'),
        ('dark', '夜間')
    )
    alert_day_choices = (
        ('Monday', '星期一'),
        ('Tuesday', '星期二'),
        ('Wednesday', '星期三'),
        ('Thursday', '星期四'),
        ('Friday', '星期五'),
        ('Saturday', '星期六'),
        ('Sunday', '星期日'),
    )

    theme = models.CharField(max_length=10, choices=theme_choices)
    anim_char_name = models.CharField(max_length=15)
    is_alerted = models.BooleanField(default=False)
    alert_day = models.JSONField(blank=True, null=True)
    alert_time = models.TimeField(blank=True, null=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

# done
class WeigthtHistory(models.Model):

    weight = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    user_id=models.ForeignKey(Users, on_delete=models.CASCADE)

# done
class NotificationHistory(models.Model):

    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    label = models.TextField(blank=True, null=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

# done
class BodyFatHistory(models.Model):

    body_fat = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    user_id=models.ForeignKey(Users, on_delete=models.CASCADE)

# done
class WaterHistory(models.Model):

    water = models.FloatField()
    date = models.DateTimeField()
    user_id=models.ForeignKey(Users, on_delete=models.CASCADE)

class Achievement(models.Model):
    label_choices = (
        ('common', '共同'),
        ('sport', '運動'),
        ('diet', '飲食')
    )

    name = models.TextField()
    description = models.TextField()
    label = models.CharField(max_length=20, choices=label_choices)
    image = models.TextField()

class UserAchievement(models.Model):
    is_achieve = models.BooleanField(default=False)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    achievement_id = models.ForeignKey(Achievement, on_delete=models.CASCADE)

class SportRecordWeek(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    seconds = models.FloatField(default=0)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

class AchievementRecord(models.Model):
    
    # 計算是否達到 bodybooster
    count_achieve = models.IntegerField(default=0)
    count_achieve_state = models.BooleanField(default=True)
    # 計算每日簽到
    continuous_bonus = models.IntegerField(default=0)
    continuous_bonus_state = models.BooleanField(default=True)
    # 紀錄飲食成就
    continuous_sodium_state = models.BooleanField(default=True)
    continuous_pfc_state = models.BooleanField(default=True)
    continuous_calorie_state = models.BooleanField(default=True)
    continuous_protein_state = models.BooleanField(default=True)
    continuous_record = models.IntegerField(default=0)
    continuous_record_state = models.BooleanField(default=True)
    # 紀錄運動成就
    sport_ten_state = models.BooleanField(default=True)
    sport_twenty_state = models.BooleanField(default=True)
    sport_all_state = models.BooleanField(default=True)

    sport_time_seventyfive_state = models.BooleanField(default=True)
    sport_time_hundredeighty_state = models.BooleanField(default=True)
    continuous_sport_seventyfive_week = models.IntegerField(default=0)
    continuous_sport_hundredeighty_week = models.IntegerField(default=0)
    sport_record_week_id = models.ForeignKey(SportRecordWeek, on_delete=models.DO_NOTHING)
    # 減重
    lose_two_weight_state = models.BooleanField(default=True)
    lose_ten_weight_state = models.BooleanField(default=True)
    
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

# class DietDayRecord(models.Model):

#     date = models.DateField(default=timezone.now)
#     calorie = models.FloatField(default=0)
#     protein = models.FloatField(default=0)
#     fat = models.FloatField(default=0)
#     carb = models.FloatField(default=0)
#     sodium = models.FloatField(default=0)
#     user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

class UserAchievedSport(models.Model):
    date = models.DateField(auto_now_add=True)
    sport_id = models.ForeignKey(Sport, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

class DietRecordDate(models.Model):
    date = models.DateField()
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
