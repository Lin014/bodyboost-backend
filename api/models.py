from django.db import models

# Create your models here.
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

    account = models.CharField(max_length=30, blank=False, null=False)
    password = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=30, blank=False, null=False)
    created_type = models.CharField(max_length=20, choices=created_type_choices, blank=False, null=False)
    status = models.CharField(max_length=20, choices=status_choices, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
