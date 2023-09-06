# Generated by Django 4.2.4 on 2023-09-06 10:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carwash', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workday',
            name='date',
            field=models.DateField(db_index=True, unique=True, verbose_name='дата'),
        ),
        migrations.CreateModel(
            name='CarWashUserRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_time', models.DateTimeField(db_index=True, unique=True, verbose_name='дата и время')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='клиент')),
                ('services', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='carwash.carwashregistration')),
            ],
            options={
                'verbose_name': 'Запись пользователя',
                'verbose_name_plural': 'Записи пользователей',
            },
        ),
    ]
