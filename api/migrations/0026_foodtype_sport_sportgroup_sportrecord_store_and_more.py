# Generated by Django 4.2.1 on 2023-05-29 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_alter_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('default_time', models.FloatField()),
                ('interval', models.FloatField()),
                ('is_count', models.BooleanField()),
                ('animation', models.FileField(upload_to='animation_video')),
                ('image', models.ImageField(upload_to='animation_img')),
                ('met', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SportGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('rest_time', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.users')),
            ],
        ),
        migrations.CreateModel(
            name='SportRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('single', '單一運動'), ('combo', '組合運動')], max_length=20)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('total_time', models.FloatField(default=0)),
                ('total_consumed_kcal', models.FloatField(default=0)),
                ('cur_sport_no', models.IntegerField(default=1)),
                ('is_record_video', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.users')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='emailverifycode',
            name='send_type',
            field=models.CharField(choices=[('register', '註冊'), ('forget', '忘記密碼')], max_length=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(upload_to='profile_img'),
        ),
        migrations.CreateModel(
            name='SportRecordItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('default_time', models.FloatField()),
                ('interval', models.FloatField()),
                ('is_count', models.BooleanField()),
                ('animation', models.FileField(upload_to='animation_video')),
                ('image', models.ImageField(upload_to='animation_img')),
                ('met', models.FloatField()),
                ('mode', models.CharField(choices=[('timing', '計時'), ('counting', '計次')], max_length=20)),
                ('time', models.FloatField(default=0)),
                ('counts', models.IntegerField(default=0)),
                ('consumed_kcal', models.FloatField(default=0)),
                ('video', models.FileField(upload_to='record_video')),
                ('sport_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.sportrecord')),
            ],
        ),
        migrations.CreateModel(
            name='SportGroupItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.CharField(choices=[('timing', '計時'), ('counting', '計次')], max_length=20)),
                ('custom_time', models.FloatField()),
                ('custom_counts', models.IntegerField()),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.sport')),
                ('sport_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.sportgroup')),
            ],
        ),
        migrations.CreateModel(
            name='SportFrequency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency', models.IntegerField()),
                ('sport', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.sport')),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calorie', models.FloatField()),
                ('size', models.FloatField()),
                ('unit', models.CharField(max_length=30)),
                ('protein', models.FloatField()),
                ('fat', models.FloatField()),
                ('carb', models.FloatField()),
                ('sodium', models.FloatField()),
                ('food_type', models.ForeignKey(on_delete=models.SET(''), to='api.foodtype')),
                ('store', models.ForeignKey(on_delete=models.SET(''), to='api.store')),
            ],
        ),
        migrations.CreateModel(
            name='DietRecordItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('calorie', models.FloatField()),
                ('size', models.FloatField()),
                ('unit', models.CharField(max_length=30)),
                ('protein', models.FloatField()),
                ('fat', models.FloatField()),
                ('carb', models.FloatField()),
                ('sodium', models.FloatField()),
                ('food_type', models.ForeignKey(on_delete=models.SET(''), to='api.foodtype')),
                ('store', models.ForeignKey(on_delete=models.SET(''), to='api.store')),
            ],
        ),
        migrations.CreateModel(
            name='DietRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('label', models.TextField()),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.dietrecorditem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.users')),
            ],
        ),
        migrations.CreateModel(
            name='CustomFood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('calorie', models.FloatField()),
                ('size', models.FloatField()),
                ('unit', models.CharField(max_length=30)),
                ('protein', models.FloatField()),
                ('fat', models.FloatField()),
                ('carb', models.FloatField()),
                ('sodium', models.FloatField()),
                ('food_type', models.ForeignKey(on_delete=models.SET(''), to='api.foodtype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.users')),
            ],
        ),
    ]
