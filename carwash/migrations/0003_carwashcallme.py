# Generated by Django 4.2.4 on 2023-09-18 10:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carwash', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarWashCallMe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '89999999999 или +79999999999'", regex='^\\+?1?\\d{9,15}$')])),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
