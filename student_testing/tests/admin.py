from django.contrib import admin
from django.urls import path
from .models import Question, Test, StudentResponse
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .views import test_report


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_short_text', 'time_create_question', 'question_type', 'klass_destination', 'topics')
    list_filter = ('time_create_question',  'question_type', 'klass_destination', 'topics')
    
    def get_short_text(self, obj):
        txt = obj.text[:40]
        for s in ['<p>', '</p>', '<em>', '</em>', '<sub>', '</sub>']:
            txt = txt.replace(s, '')
        txt = txt.replace('&nbsp;', ' ')
        return txt + '...' if len(obj.text) > 50 else obj.text  # Сокращаем до 50 символов
    
    get_short_text.short_description = 'Текст'  # Устанавливаем заголовок для столбца
    
    class Media:
        css = {
            'all': ('css/admin_custom.css',)  # Укажите путь к вашему CSS файлу
        }


class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_create_test', 'klass_destination', 'repeated_answer')
    list_filter = ('title', 'time_create_test', 'klass_destination', 'repeated_answer')
    class Media:
        css = {
            'all': ('css/admin_custom.css',)  # Укажите путь к вашему CSS файлу
        }


class StudentResponseAdmin(admin.ModelAdmin):
    list_display = ('test', 'student', 'time_answer', 'get_results_questions_student', 'score')
    # list_filter = ('test', 'student', 'time_answer', 'score')
    list_filter = ('test', 'time_answer')
    # actions = [export_test_results]  # Добавляем действие
    
    def get_results_questions_student(self, obj):
        return obj.right_answer

    get_results_questions_student.short_description = 'Результаты'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('test-report/', self.admin_site.admin_view(test_report), name='test_report'),
        ]
        return custom_urls + urls





admin.site.register(Question, QuestionAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(StudentResponse, StudentResponseAdmin)

    
    
    
