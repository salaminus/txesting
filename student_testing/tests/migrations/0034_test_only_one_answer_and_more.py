# Generated by Django 5.1.6 on 2025-03-16 16:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0033_alter_question_time_create_question_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='only_one_answer',
            field=models.BooleanField(default=True, verbose_name='Принимать только первый ответ'),
        ),
        migrations.AlterField(
            model_name='question',
            name='time_create_question',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 16, 19, 17, 58, 919379), verbose_name='Создано'),
        ),
        migrations.AlterField(
            model_name='studentresponse',
            name='time_answer',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 16, 19, 17, 58, 920949), verbose_name='Создано'),
        ),
        migrations.AlterField(
            model_name='test',
            name='repeated_answer',
            field=models.BooleanField(default=False, verbose_name='Разрешена отправка'),
        ),
        migrations.AlterField(
            model_name='test',
            name='time_create_test',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 16, 19, 17, 58, 919857), verbose_name='Создано'),
        ),
    ]
