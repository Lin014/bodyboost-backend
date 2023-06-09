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

# done
class Profile(models.Model):
    gender_choices = [(1, 1), (2, 2)]

    name = models.CharField(max_length=50)
    gender = models.IntegerField(choices=gender_choices)
    birthday = models.DateField()
    height = models.FloatField()
    weight = models.FloatField()
    image = models.ImageField(upload_to='profile_img', default='')
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
    name = models.TextField()

# done
class FoodType(models.Model):
    type = models.TextField()

# done
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
class CustomFood(models.Model):
    name = models.TextField()
    calorie = models.FloatField()
    size = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=30, blank=True, null=True)
    protein = models.FloatField(blank=True, null=True)
    fat = models.FloatField(blank=True, null=True)
    carb = models.FloatField(blank=True, null=True)
    sodium = models.FloatField(blank=True, null=True)
    food_type_id = models.ForeignKey(FoodType, on_delete=models.SET(''))
    store_id = models.ForeignKey(Store, on_delete=models.SET(''))
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

# done
class DietRecord(models.Model):
    date = models.DateTimeField()
    serving_amount = models.FloatField(blank=True, null=True) #
    label = models.TextField(blank=True, null=True)
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

class Sport(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    default_time = models.FloatField()
    interval = models.FloatField()
    is_count = models.BooleanField()
    animation = models.FileField(upload_to='animation_video')
    image = models.ImageField(upload_to='animation_img')
    met = models.FloatField()

class SportFrequency(models.Model):
    frequency = models.IntegerField()
    sport = models.OneToOneField(Sport, on_delete=models.CASCADE)

class SportGroup(models.Model):
    name = models.TextField()
    rest_time = models.FloatField()
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

class SportGroupItem(models.Model):
    mode_choices = (
        ('timing', '計時'),
        ('counting', '計次')
    )

    mode = models.CharField(max_length=20, choices=mode_choices)
    custom_time = models.FloatField()
    custom_counts = models.IntegerField(blank=True, null=True)
    sport_id = models.ForeignKey(Sport, on_delete=models.CASCADE)
    sport_group_id = models.ForeignKey(SportGroup, on_delete=models.CASCADE)

class SportRecord(models.Model):
    type_choices = (
        ('single', '單一運動'),
        ('combo', '組合運動')
    )

    type = models.CharField(max_length=20, choices=type_choices)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    total_time = models.FloatField(default=0)
    total_consumed_kcal = models.FloatField(default=0)
    cur_sport_no = models.IntegerField(default=1)
    is_record_video = models.BooleanField(default=False)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

class SportRecordItem(models.Model):
    mode_choices = (
        ('timing', '計時'),
        ('counting', '計次')
    )

    # copy sport field
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    default_time = models.FloatField()
    interval = models.FloatField()
    is_count = models.BooleanField()
    animation = models.FileField(upload_to='animation_video')
    image = models.ImageField(upload_to='animation_img')
    met = models.FloatField()
    # other field
    mode = models.CharField(max_length=20, choices=mode_choices)
    time = models.FloatField(default=0)
    counts = models.IntegerField(default=0)
    consumed_kcal = models.FloatField(default=0)
    sport_record_id = models.ForeignKey(SportRecord, on_delete=models.CASCADE)
    video = models.FileField(upload_to='record_video', blank=True, null=True)