# Generated by Django 4.2.2 on 2023-07-11 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0038_remove_dietrecord_dietrecorditem_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dietrecord',
            old_name='time',
            new_name='date',
        ),
    ]
