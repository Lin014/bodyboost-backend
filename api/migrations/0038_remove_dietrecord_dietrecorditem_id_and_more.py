# Generated by Django 4.2.2 on 2023-07-11 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_food_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dietrecord',
            name='dietRecordItem_id',
        ),
        migrations.AddField(
            model_name='dietrecord',
            name='calorie',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dietrecord',
            name='carb',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dietrecord',
            name='fat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dietrecord',
            name='food_type_id',
            field=models.ForeignKey(default=2, on_delete=models.SET(''), to='api.foodtype'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dietrecord',
            name='name',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dietrecord',
            name='protein',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dietrecord',
            name='size',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dietrecord',
            name='sodium',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dietrecord',
            name='store_id',
            field=models.ForeignKey(default=0, on_delete=models.SET(''), to='api.store'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dietrecord',
            name='unit',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.DeleteModel(
            name='DietRecordItem',
        ),
    ]
