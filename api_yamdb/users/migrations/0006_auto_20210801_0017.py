# Generated by Django 2.2.6 on 2021-07-31 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210730_0153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('u', 'user'), ('m', 'moderator'), ('a', 'admin')], default=('u', 'user'), max_length=16, verbose_name='Права доступа'),
        ),
    ]
