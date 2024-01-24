# Generated by Django 4.2.7 on 2023-11-23 21:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('carwash', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='carwashregistration',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='клиент'),
        ),
        migrations.AddField(
            model_name='carwashregistration',
            name='services',
            field=models.ManyToManyField(to='carwash.carwashservice', verbose_name='услуги'),
        ),
    ]
