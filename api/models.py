from django.db import models
from datetime import date

class users(models.Model):
    status_choices = [ 
        ('success', 'Success'), 
        ('verified', 'Verified'), 
        ('unverified', 'Unverified') 
    ]
    created_type_choices = [ 
        ('normal', 'Normal'),
        ('google', "Google") 
    ]

    account = models.CharField(max_length=30)
    password = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField()
    created_type = models.CharField(max_length=20, choices=created_type_choices)
    status = models.CharField(max_length=20, choices=status_choices)
    created_at = models.DateTimeField(auto_now_add=True)

class profile(models.Model):
    gender_choices = [(1, 'Male'), (2, 'Female')]

    name = models.CharField(max_length=50)
    gender = models.IntegerField(choices=gender_choices)
    birthday = models.DateField()
    height = models.FloatField()
    weight = models.FloatField()
    image = models.TextField(blank=True, null=True)
    user_id = models.OneToOneField(users, on_delete=models.CASCADE)

class EmailVerifyCode(models.Model):
    send_type_choices = (
        ('register', 'Register'),
        ('forget', 'Forget')
    )
    code = models.CharField(max_length=15)
    email = models.EmailField()
    send_type = models.CharField(max_length=20, choices=send_type_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(users, on_delete=models.CASCADE)

