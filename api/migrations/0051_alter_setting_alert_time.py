# Generated by Django 4.2.2 on 2023-07-22 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0050_setting_alert_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='alert_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
