# Generated by Django 4.2.4 on 2023-08-24 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Логин')),
                ('fio', models.CharField(blank=True, max_length=255, verbose_name='ФИО')),
                ('tel', models.CharField(blank=True, max_length=15, verbose_name='телефон')),
                ('car_type', models.CharField(choices=[('price_standart', 'седан, хетчбэк'), ('price_crossover', 'кроссовер'), ('price_offroad', 'внедорожник')], default='price_standart', max_length=40, verbose_name='тип автомобиля')),
                ('car_model', models.CharField(blank=True, max_length=150, verbose_name='марка и модель автомобиля')),
                ('discount', models.SmallIntegerField(default=0, verbose_name='дисконт')),
                ('user_creation_date', models.DateTimeField(auto_now_add=True, verbose_name='дата регистрации пользователя')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
