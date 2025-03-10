# tests/forms.py
from django import forms
from .models import Question, Test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class TestResponseForm(forms.Form):
    # Здесь динамически добавлятся поля для ответов на вопросы во время тестирования
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', None)
        super(TestResponseForm, self).__init__(*args, **kwargs)
        if questions:
            for question in questions:
                self.fields[f'question_{question.id}'] = forms.CharField(
                    label={'id': question.id, 
                           'text': question.text,
                           'file': question.file},
                    widget=forms.TextInput(),
                    # widget=forms.TextInput(attrs={'placeholder': 'Ответ'}),
                )
                
                
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = [
                    'title' , 
                    'questions', 
                    'klass_destination', 
                    'repeated_answer',
                    'tmp'
                ]
    


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
                    'text', 
                    'file',
                    'topics',
                    'question_type', 
                    'correct_answer',
                    'klass_destination'
                ]
    
    