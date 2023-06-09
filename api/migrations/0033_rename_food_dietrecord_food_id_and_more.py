# Generated by Django 4.2.2 on 2023-07-05 04:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_rename_food_type_customfood_food_type_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dietrecord',
            old_name='food',
            new_name='food_id',
        ),
        migrations.RenameField(
            model_name='dietrecord',
            old_name='user',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='dietrecorditem',
            old_name='food_type',
            new_name='food_type_id',
        ),
        migrations.RenameField(
            model_name='dietrecorditem',
            old_name='store',
            new_name='store_id',
        ),
        migrations.RenameField(
            model_name='emailverifycode',
            old_name='user',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='food',
            old_name='food_type',
            new_name='food_type_id',
        ),
        migrations.RenameField(
            model_name='food',
            old_name='store',
            new_name='store_id',
        ),
        migrations.RenameField(
            model_name='sportgroup',
            old_name='user',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='sportgroupitem',
            old_name='sport_group',
            new_name='sport_group_id',
        ),
        migrations.RenameField(
            model_name='sportgroupitem',
            old_name='sport',
            new_name='sport_id',
        ),
        migrations.RenameField(
            model_name='sportrecord',
            old_name='user',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='sportrecorditem',
            old_name='sport_record',
            new_name='sport_record_id',
        ),
    ]
