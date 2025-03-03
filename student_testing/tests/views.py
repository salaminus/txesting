import pprint
from django.shortcuts import get_object_or_404, render, redirect
from .models import Test, StudentResponse
from django.contrib.auth.decorators import login_required
from .forms import TestResponseForm, UserRegisterForm, UserLoginForm
from django.contrib.auth import login, authenticate


@login_required
def test_list(request):
    # Группы ученика
    student_groups = [gr.name for gr in list(request.user.groups.all())]
    # print(student_groups)
    # tests = Test.objects.filter()
    tests = Test.objects.filter(klass_destination=student_groups[0]) # Отбор тестов по группе ученика
    # print(tests.values('klass_destination'))
    status_testing_for_user = StudentResponse.objects.filter(student_id=request.user.id)
    tests_set = set([item['id'] for item in list(tests.values('id'))])
    status_set = set([item['test_id'] for item in list(status_testing_for_user.values('test_id'))])
    status_testing_for_user = tests_set.difference(status_set)
    # print(status_testing_for_user)
    # Если уже проходил и отключена повторная отправка - закрыть тест
    return render(request, 'tests/test_list.html', {
                                'tests': tests,
                                'status_testing_for_user': status_testing_for_user})

@login_required
def take_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)

    if request.method == 'POST':
        form = TestResponseForm(request.POST, questions=test.questions.all())
        if form.is_valid():
            # Сохраняем ответы в формате словаря
            answers = {key: form.cleaned_data[key] for key in form.cleaned_data}
            response = StudentResponse(student=request.user, test=test, answers=answers)
            answer_correct_db = dict(test.questions.all().values_list('id', 'correct_answer'))
            answers_student = dict([(int(k[-1]), v) for k, v in answers.items()])
            answers_correct_student_for_db = {k: answers_student[k]==answer_correct_db[k] for k, v in answers_student.items()}
            score = sum([int(v) for v in answers_correct_student_for_db.values()]) # Итог
            response.right_answer = answers_correct_student_for_db
            response.score = score
            response.save()
            return redirect('test_results', response.id)
    else:
        form = TestResponseForm(questions=test.questions.all())

    return render(request, 'tests/take_test.html', {'test': test, 'form': form})


@login_required
def test_results(request, response_id):
    response = get_object_or_404(StudentResponse, id=response_id)
    return render(request, 'tests/test_results.html', {'response': response})


def home(request):
    return render(request, 'tests/home.html')

@login_required
def test_students_results(request, test_id):
    test_title = Test.objects.filter(id=test_id)[0].title
    test_klass = Test.objects.filter(id=test_id)[0].klass_destination
    results = StudentResponse.objects.filter(test_id=test_id)
    
    
    return render(request, 'tests/test_students_results.html', 
                  {'results': results, 
                   'test_title': test_title,
                   'test_klass': test_klass})


@login_required
def user_test_results(request):
    if request.user.is_authenticated:
        results = StudentResponse.objects.filter(student_id=request.user.id)
        return render(request, 'tests/my_tests.html', {'results': results})
    else:
        return redirect('login')  # Перенаправление на страницу входа, если пользователь не аутентифицирован
    

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Замените 'home' на ваше целевое представление
    else:
        form = UserRegisterForm()
    return render(request, 'tests/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Замените 'home' на ваше целевое представление
    else:
        form = UserLoginForm()
    return render(request, 'tests/login.html', {'form': form})



# TODO: Проверка, если уже проходил и отключена повторная отправка - закрыть тест +++
# TODO: Отсечь тесты по классам: чужие тесты убрать из списка тестов +++
# TODO: WYSYWIG редактор тестов ---