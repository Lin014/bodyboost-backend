# Generated by Django 4.2.2 on 2023-07-23 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0051_alter_setting_alert_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='goal',
            field=models.CharField(default='health', max_length=30),
            preserve_default=False,
        ),
    ]