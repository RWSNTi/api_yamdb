# Generated by Django 2.2.6 on 2021-07-29 22:06

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_merge_20210729_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationemail',
            name='confirmation_code',
            field=models.CharField(max_length=10, verbose_name='Код подтверждения'),
        ),
        migrations.AlterField(
            model_name='registrationemail',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email адрес'),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Информация о пользователе'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email адрес'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=25, verbose_name='Пароль'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')], default=('user', 'user'), max_length=16, verbose_name='Права доступа'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'Пользователь с этим именем уже существует.'}, help_text='Обязательное поле, только цифры, буквы или @/./+/-/_.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='Псевдоним'),
        ),
    ]
