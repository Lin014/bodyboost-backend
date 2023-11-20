# Generated by Django 4.2.2 on 2023-08-20 03:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0085_achievementrecord_continuous_record_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DietRecordDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.users')),
            ],
        ),
    ]
