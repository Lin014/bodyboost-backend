# Generated by Django 4.2.2 on 2023-07-11 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_remove_food_carb_remove_food_fat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='carb',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='food',
            name='fat',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='food',
            name='food_type_id',
            field=models.ForeignKey(default=0, on_delete=models.SET(''), to='api.foodtype'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='food',
            name='protein',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='food',
            name='size',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='food',
            name='sodium',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='food',
            name='store_id',
            field=models.ForeignKey(default=0, on_delete=models.SET(''), to='api.store'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='food',
            name='unit',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
    ]
