# Generated by Django 4.2.2 on 2023-07-19 06:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0042_rename_default_time_sportrecorditem_custom_time_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(choices=[('light', '日間'), ('dark', '夜間')], max_length=10)),
                ('anim_char_name', models.CharField(max_length=15)),
                ('is_alerted', models.BooleanField(default=False)),
                ('alert_time', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='sportrecorditem',
            name='custom_counts',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sportrecord',
            name='start_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='sportrecorditem',
            name='custom_time',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='AnimatedCharacter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('animation', models.FileField(upload_to='animation_video')),
                ('image', models.ImageField(upload_to='animation_img')),
                ('sport_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.sport')),
            ],
        ),
        migrations.CreateModel(
            name='Accuracy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accuracy', models.FloatField()),
                ('label', models.CharField(max_length=15)),
                ('sport_record_item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.sportrecorditem')),
            ],
        ),
    ]
