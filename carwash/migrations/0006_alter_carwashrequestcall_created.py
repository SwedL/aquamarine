# Generated by Django 4.2.4 on 2023-09-29 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carwash', '0005_alter_carwashrequestcall_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carwashrequestcall',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='создан'),
        ),
    ]