# Generated by Django 4.2.1 on 2023-05-24 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_alter_profile_exercise_degree_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='exercise_degree_id',
        ),
    ]
