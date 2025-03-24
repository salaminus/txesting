# tests/forms.py
from django import forms
from .models import Question, Test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group

class TestResponseForm(forms.Form):
    # Здесь динамически добавлятся поля для ответов на вопросы во время тестирования
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', None)
        super(TestResponseForm, self).__init__(*args, **kwargs)
        if questions:
            for question in questions:
                self.fields[f'question_{question.id}'] = forms.CharField(
                    label={
                            'id': question.id, 
                            'text': question.text,
                            'file': question.file,
                            'question_type': question.question_type,
                        },
                
                        widget=forms.TextInput(),
                        # widget=forms.TextInput(attrs={'placeholder': 'Ответ'}),
                    )
                
                
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    klass_user = forms.ModelChoiceField(queryset=Group.objects.exclude(name='teachers'), 
                                        label="Класс",
                                        required=True)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Связь usera с группой (классом)
            group = self.cleaned_data['klass_user']
            group.user_set.add(user)
        return user

    class Meta:
        model = User
        fields = ['username', 
                  'first_name', 
                  'last_name', 
                  'email', 
                  'password1', 
                  'password2', 
                  'klass_user']

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
                    'only_one_answer',
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
    
    