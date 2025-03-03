from django.contrib import admin
from .models import Question, Test, StudentResponse
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'time_create_question', 'question_type', 'klass_destination', 'topics')
    list_filter = ('time_create_question',  'question_type', 'klass_destination', 'topics')


class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_create_test', 'klass_destination', 'repeated_answer')
    list_filter = ('title', 'time_create_test', 'klass_destination', 'repeated_answer')


class StudentResponseAdmin(admin.ModelAdmin):
    list_display = ('test', 'student', 'time_answer', 'score')
    list_filter = ('test', 'student', 'time_answer', 'score')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(StudentResponse, StudentResponseAdmin)

    
    
    
