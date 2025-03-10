import datetime
from django.db import models
from django.contrib.auth.models import User
from .CONFIGS_APP import TOPICS, CLASSES, QUESTION_TYPES
from ckeditor.fields import RichTextField


class Question(models.Model):
    # text = models.TextField(verbose_name='Текст') # Содержание вопроса
    text = RichTextField(verbose_name='Текст')
    file = models.URLField(verbose_name='Ссылка на файл', blank=True)
    # theme = models.TextField(default='') # Тема вопроса
    question_type = models.CharField(default='SA', max_length=2, choices=QUESTION_TYPES, verbose_name='Тип вопроса')
    correct_answer = models.CharField(max_length=256, verbose_name='Правильный ответ')
    time_create_question = models.DateTimeField(default=datetime.datetime.now(), verbose_name='Создано')
    klass_destination = models.CharField(default='7', max_length=2, choices=CLASSES, verbose_name='Класс')
    topics = models.CharField(max_length=128, default='Txt', choices=TOPICS, verbose_name='Тема')
    
    def __str__(self):
        import re
        html_code = self.text
        text = re.sub(r'<[^>]+>', '', html_code)
        text = re.sub(r'&[a-zA-Z0-9#]+;', '', text)
        return text[:130] + '...' + f'[{self.klass_destination}]'

class Test(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    questions = models.ManyToManyField(Question, verbose_name='Вопросы')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    time_create_test = models.DateTimeField(default=datetime.datetime.now(), verbose_name='Создано')
    klass_destination = models.CharField(default='7', max_length=2, choices=CLASSES, verbose_name='Класс')
    repeated_answer = models.BooleanField(default=False, verbose_name='Повторные ответы')
    tmp = models.BooleanField(default=True, verbose_name='Без заданий (временный тест)')

    def __str__(self):
        return self.title

class StudentResponse(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Учащийся')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Тест')
    answers = models.JSONField(verbose_name='Ответы')  # Ответы как JSON
    score = models.FloatField(null=True, blank=True, verbose_name='Набрано')
    time_answer = models.DateTimeField(default=datetime.datetime.now(), verbose_name='Создано')
    right_answer = models.JSONField(verbose_name='Правильный ответ')

    def __str__(self):
        return f"{self.student.username} - {self.test.title}"


    