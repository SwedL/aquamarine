# Generated by Django 4.2.7 on 2023-11-16 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carwash', '0006_alter_workday_time_1000_alter_workday_time_1030_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workday',
            name='time_1000',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time1', to='carwash.carwashregistration'),
        ),
        migrations.AlterField(
            model_name='workday',
            name='time_1030',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time2', to='carwash.carwashregistration'),
        ),
        migrations.AlterField(
            model_name='workday',
            name='time_1100',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time3', to='carwash.carwashregistration'),
        ),
        migrations.AlterField(
            model_name='workday',
            name='time_1130',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time4', to='carwash.carwashregistration'),
        ),
        migrations.AlterField(
            model_name='workday',
            name='time_1200',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time5', to='carwash.carwashregistration'),
        ),
        migrations.AlterField(
            model_name='workday',
            name='time_1230',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time6', to='carwash.carwashregistration'),
        ),
        migrations.AlterField(
            model_name='workday',
            name='time_1300',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time7', to='carwash.carwashregistration'),
        ),
        migrations.AlterField(
            model_name='workday',
            name='time_1330',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time8', to='carwash.carwashregistration'),
        ),
        migrations.AlterField(
            model_name='workday',
            name='time_1400',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time9', to='carwash.carwashregistration'),
        ),
        migrations.AlterField(
            model_name='workday',
            name='time_1430',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time10', to='carwash.carwashregistration'),
        ),
        migrations.AlterField(
            model_name='workday',
            name='time_1500',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time11', to='carwash.carwashregistration'),
        ),
        migrations.AlterField(
            model_name='workday',
            name='time_1530',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time12', to='carwash.carwashregistration'),
        ),
        migrations.AlterField(
            model_name='workday',
            name='time_1600',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time13', to='carwash.carwashregistration'),
        ),
        migrations.AlterField(
            model_name='workday',
            name='time_1630',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time14', to='carwash.carwashregistration'),
        ),
        migrations.AlterField(
            model_name='workday',
            name='time_1700',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time15', to='carwash.carwashregistration'),
        ),
        migrations.AlterField(
            model_name='workday',
            name='time_1730',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time16', to='carwash.carwashregistration'),
        ),
        migrations.AlterField(
            model_name='workday',
            name='time_1800',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time17', to='carwash.carwashregistration'),
        ),
        migrations.AlterField(
            model_name='workday',
            name='time_1830',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time18', to='carwash.carwashregistration'),
        ),
        migrations.AlterField(
            model_name='workday',
            name='time_1900',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time19', to='carwash.carwashregistration'),
        ),
        migrations.AlterField(
            model_name='workday',
            name='time_1930',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time20', to='carwash.carwashregistration'),
        ),
        migrations.AlterField(
            model_name='workday',
            name='time_2000',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time21', to='carwash.carwashregistration'),
        ),
        migrations.AlterField(
            model_name='workday',
            name='time_2030',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time22', to='carwash.carwashregistration'),
        ),
    ]
