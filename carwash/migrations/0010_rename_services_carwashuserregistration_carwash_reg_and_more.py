# Generated by Django 4.2.4 on 2023-10-05 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carwash', '0009_alter_carwashuserregistration_services'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carwashuserregistration',
            old_name='services',
            new_name='carwash_reg',
        ),
        migrations.AlterField(
            model_name='carwashuserregistration',
            name='date_reg',
            field=models.DateField(verbose_name='дата записи'),
        ),
        migrations.AlterField(
            model_name='carwashuserregistration',
            name='time_reg',
            field=models.TimeField(verbose_name='время записи'),
        ),
    ]
