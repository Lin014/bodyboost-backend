# Generated by Django 4.2.2 on 2023-07-12 04:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0040_dietrecord_modify_dietrecord_serving_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailybonus',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]