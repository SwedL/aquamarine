# Generated by Django 5.2 on 2025-04-10 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carwash', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carwashregistration',
            name='total_cost',
            field=models.PositiveIntegerField(default=0, verbose_name='общая стоимость'),
        ),
    ]
