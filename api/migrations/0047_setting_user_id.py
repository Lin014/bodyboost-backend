# Generated by Django 4.2.2 on 2023-07-22 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0046_rename_animatedcharacter_animation'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.users'),
            preserve_default=False,
        ),
    ]