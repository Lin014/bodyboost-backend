# Generated by Django 4.2.1 on 2023-05-23 04:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_rename_exercise_degree_profile_exercise_degree_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.users'),
        ),
    ]
