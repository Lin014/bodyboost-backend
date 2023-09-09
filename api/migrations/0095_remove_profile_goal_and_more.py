# Generated by Django 4.2.2 on 2023-08-22 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0094_achievementrecord_continuous_sport_hundredeighty_week_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='goal',
        ),
        migrations.AddField(
            model_name='achievementrecord',
            name='lose_ten_weight_state',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='achievementrecord',
            name='lose_two_weight_state',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='goal_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='api.goalhistory'),
            preserve_default=False,
        ),
    ]