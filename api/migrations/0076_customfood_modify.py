# Generated by Django 4.2.2 on 2023-08-16 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0075_remove_dietrecord_serving_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='customfood',
            name='modify',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
