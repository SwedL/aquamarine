# Generated by Django 4.2.6 on 2023-10-30 10:37

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarWashRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Запись',
                'verbose_name_plural': 'Записи',
            },
        ),
        migrations.CreateModel(
            name='CarWashRequestCall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='Номер телефона должен быть в формате: "89999999999"', regex='8\\d{10}$')], verbose_name='номер телефона')),
                ('processed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='создан')),
            ],
            options={
                'verbose_name': 'Request Call',
                'verbose_name_plural': 'Request Call',
            },
        ),
        migrations.CreateModel(
            name='CarWashService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, unique=True, verbose_name='название')),
                ('process_time', models.SmallIntegerField(default=0, verbose_name='длительность')),
                ('price_standart', models.IntegerField(default=0, verbose_name='седан, хетчбэк')),
                ('price_crossover', models.IntegerField(default=0, verbose_name='кроссовер')),
                ('price_offroad', models.IntegerField(default=0, verbose_name='внедорожник')),
            ],
            options={
                'verbose_name': 'Услугу',
                'verbose_name_plural': 'Услуги',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='WorkDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_index=True, unique=True, verbose_name='дата')),
                ('time_1000', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time1', to='carwash.carwashregistration')),
                ('time_1030', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time2', to='carwash.carwashregistration')),
                ('time_1100', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time3', to='carwash.carwashregistration')),
                ('time_1130', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time4', to='carwash.carwashregistration')),
                ('time_1200', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time5', to='carwash.carwashregistration')),
                ('time_1230', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time6', to='carwash.carwashregistration')),
                ('time_1300', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time7', to='carwash.carwashregistration')),
                ('time_1330', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time8', to='carwash.carwashregistration')),
                ('time_1400', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time9', to='carwash.carwashregistration')),
                ('time_1430', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time10', to='carwash.carwashregistration')),
                ('time_1500', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time11', to='carwash.carwashregistration')),
                ('time_1530', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time12', to='carwash.carwashregistration')),
                ('time_1600', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time13', to='carwash.carwashregistration')),
                ('time_1630', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time14', to='carwash.carwashregistration')),
                ('time_1700', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time15', to='carwash.carwashregistration')),
                ('time_1730', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time16', to='carwash.carwashregistration')),
                ('time_1800', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time17', to='carwash.carwashregistration')),
                ('time_1830', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time18', to='carwash.carwashregistration')),
                ('time_1900', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time19', to='carwash.carwashregistration')),
                ('time_1930', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time20', to='carwash.carwashregistration')),
                ('time_2000', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time21', to='carwash.carwashregistration')),
                ('time_2030', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time22', to='carwash.carwashregistration')),
            ],
            options={
                'verbose_name': 'Рабочий день',
                'verbose_name_plural': 'Рабочие дни',
            },
        ),
        migrations.CreateModel(
            name='CarWashUserRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_reg', models.DateField(verbose_name='дата записи')),
                ('time_reg', models.TimeField(verbose_name='время записи')),
                ('carwash_reg', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='carwash.carwashregistration')),
            ],
            options={
                'verbose_name': 'Запись пользователя',
                'verbose_name_plural': 'Записи пользователей',
            },
        ),
    ]
