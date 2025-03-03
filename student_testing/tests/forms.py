# tests/forms.py
from django import forms
    
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class TestResponseForm(forms.Form):
    # Здесь мы будем динамически добавлять поля для ответов на вопросы
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