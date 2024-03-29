# Generated by Django 4.2.2 on 2023-08-19 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0082_userachievedsport_user_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sportrecorditem',
            name='custom_counts',
        ),
        migrations.RemoveField(
            model_name='sportrecorditem',
            name='custom_time',
        ),
        migrations.RemoveField(
            model_name='sportrecorditem',
            name='description',
        ),
        migrations.RemoveField(
            model_name='sportrecorditem',
            name='interval',
        ),
        migrations.RemoveField(
            model_name='sportrecorditem',
            name='is_count',
        ),
        migrations.RemoveField(
            model_name='sportrecorditem',
            name='met',
        ),
        migrations.RemoveField(
            model_name='sportrecorditem',
            name='name',
        ),
        migrations.AddField(
            model_name='sportrecorditem',
            name='sport_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='api.sport'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sport',
            name='type',
            field=models.CharField(choices=[('aerobics', '有氧'), ('anaerobic', '無氧')], max_length=10),
        ),
    ]
