# Generated by Django 4.2.2 on 2023-07-24 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0052_profile_goal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='member_type',
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_type', models.CharField(choices=[('normal', 'Normal'), ('premium', 'Premium')], default='normal', max_length=10)),
                ('phone', models.CharField(blank=True, max_length=10, null=True)),
                ('is_trial', models.BooleanField(default=False)),
                ('payment_type', models.CharField(blank=True, max_length=15, null=True)),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.users')),
            ],
        ),
    ]
