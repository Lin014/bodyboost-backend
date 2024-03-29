# Generated by Django 4.2.2 on 2023-08-17 11:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0077_dietdayrecord_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='achievementrecord',
            name='continuous_calorie',
        ),
        migrations.RemoveField(
            model_name='achievementrecord',
            name='continuous_pfc',
        ),
        migrations.RemoveField(
            model_name='achievementrecord',
            name='continuous_sodium',
        ),
        migrations.AddField(
            model_name='achievementrecord',
            name='continuous_calorie_state',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='achievementrecord',
            name='continuous_pfc_state',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='achievementrecord',
            name='continuous_sodium_state',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='dietdayrecord',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
