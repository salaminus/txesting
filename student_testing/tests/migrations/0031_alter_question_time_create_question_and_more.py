# Generated by Django 5.1.6 on 2025-03-06 18:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0030_test_tmp_alter_question_time_create_question_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='time_create_question',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 6, 21, 38, 46, 744691), verbose_name='Создано'),
        ),
        migrations.AlterField(
            model_name='studentresponse',
            name='time_answer',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 6, 21, 38, 46, 746157), verbose_name='Создано'),
        ),
        migrations.AlterField(
            model_name='test',
            name='time_create_test',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 6, 21, 38, 46, 745218), verbose_name='Создано'),
        ),
    ]
