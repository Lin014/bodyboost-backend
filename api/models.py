from django.db import models
from datetime import date

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

class Profile(models.Model):
    gender_choices = [(1, 'Male'), (2, 'Female')]

    name = models.CharField(max_length=50)
    gender = models.IntegerField(choices=gender_choices)
    birthday = models.DateField()
    height = models.FloatField()
    weight = models.FloatField()
    image = models.ImageField(upload_to='profile_img', blank=False, null=False)
    user = models.OneToOneField(Users, on_delete=models.CASCADE)

class EmailVerifyCode(models.Model):
    send_type_choices = (
        ('register', '註冊'),
        ('forget', '忘記密碼')
    )
    code = models.CharField(max_length=15)
    email = models.EmailField()
    send_type = models.CharField(max_length=20, choices=send_type_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

class Store(models.Model):
    name = models.TextField()

class FoodType(models.Model):
    type = models.TextField()

class Food(models.Model):
    name = models.TextField
    calorie = models.FloatField()
    size = models.FloatField()
    unit = models.CharField(max_length=30)
    protein = models.FloatField()
    fat = models.FloatField()
    carb = models.FloatField()
    sodium = models.FloatField()
    food_type = models.ForeignKey(FoodType, on_delete=models.SET(''))
    store = models.ForeignKey(Store, on_delete=models.SET(''))

class CustomFood(models.Model):
    name = models.TextField()
    calorie = models.FloatField()
    size = models.FloatField(blank=False, null=False)
    unit = models.CharField(max_length=30, blank=False, null=False)
    protein = models.FloatField(blank=False, null=False)
    fat = models.FloatField(blank=False, null=False)
    carb = models.FloatField(blank=False, null=False)
    sodium = models.FloatField(blank=False, null=False)
    food_type = models.ForeignKey(FoodType, on_delete=models.SET(''))
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

class DietRecordItem(models.Model):
    name = models.TextField()
    calorie = models.FloatField()
    size = models.FloatField(blank=False, null=False)
    unit = models.CharField(max_length=30, blank=False, null=False)
    protein = models.FloatField(blank=False, null=False)
    fat = models.FloatField(blank=False, null=False)
    carb = models.FloatField(blank=False, null=False)
    sodium = models.FloatField(blank=False, null=False)
    food_type = models.ForeignKey(FoodType, on_delete=models.SET(''))
    store = models.ForeignKey(Store, on_delete=models.SET(''), blank=False, null=False)

class DietRecord(models.Model):
    time = models.DateTimeField()
    label = models.TextField(blank=False, null=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    food = models.ForeignKey(DietRecordItem, on_delete=models.CASCADE)

class Sport(models.Model):
    name = models.TextField()
    description = models.TextField(blank=False, null=False)
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
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

class SportGroupItem(models.Model):
    mode_choices = (
        ('timing', '計時'),
        ('counting', '計次')
    )

    mode = models.CharField(max_length=20, choices=mode_choices)
    custom_time = models.FloatField()
    custom_counts = models.IntegerField(blank=False, null=False)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    sport_group = models.ForeignKey(SportGroup, on_delete=models.CASCADE)

class SportRecord(models.Model):
    type_choices = (
        ('single', '單一運動'),
        ('combo', '組合運動')
    )

    type = models.CharField(max_length=20, choices=type_choices)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=False, null=False)
    total_time = models.FloatField(default=0)
    total_consumed_kcal = models.FloatField(default=0)
    cur_sport_no = models.IntegerField(default=1)
    is_record_video = models.BooleanField(default=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

class SportRecordItem(models.Model):
    mode_choices = (
        ('timing', '計時'),
        ('counting', '計次')
    )

    # copy sport field
    name = models.TextField()
    description = models.TextField(blank=False, null=False)
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
    sport_record = models.ForeignKey(SportRecord, on_delete=models.CASCADE)
    video = models.FileField(upload_to='record_video', blank=False, null=False)