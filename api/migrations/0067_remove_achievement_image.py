# Generated by Django 4.2.2 on 2023-08-13 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0066_remove_achievement_is_achieve_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='achievement',
            name='image',
        ),
    ]
