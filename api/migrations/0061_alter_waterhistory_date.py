# Generated by Django 4.2.2 on 2023-08-09 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0060_waterhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waterhistory',
            name='date',
            field=models.DateTimeField(),
        ),
    ]