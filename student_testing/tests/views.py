import pprint
from django.shortcuts import get_object_or_404, render, redirect
from .models import Test, StudentResponse, Question
from django.contrib.auth.decorators import login_required
from .forms import TestForm, TestResponseForm, UserRegisterForm, \
                    UserLoginForm, QuestionForm
from django.contrib.auth import login, authenticate
from .quest_hesh_create import calculate_hash


@login_required
def test_list(request):
    # Группы ученика
    student_groups = [gr.name for gr in list(request.user.groups.all())]
    # Отбор тестов по группе ученика
    tests = Test.objects.filter(klass_destination=student_groups[0], tmp=0) 
    # print(tests)
    # status_testing_for_user = StudentResponse.objects.filter(student_id=request.user.id)
    # print(status_testing_for_user)
    # tests_set = set([item['id'] for item in list(tests.values('id'))])
    # status_set = set([item['test_id'] for item in list(status_testing_for_user.values('test_id'))])
    # status_testing_for_user = tests_set.difference(status_set)
    # print(status_testing_for_user)
    
    stat_tests_user = StudentResponse.objects.filter(student_id=request.user.id)
    data = {tst.id: (tst, True if stat_tests_user.filter(test_id=tst.id).exists() and not tst.only_one_answer else False) for tst in tests}
    print(data)
    
    
    return render(request, 'tests/test_list.html', {
                                    'data': data,
                                })


@login_required
def test_list_admin(request):
    tests = Test.objects.exclude(tmp=True) # Отбор всех тестов без tmp==True
    results = StudentResponse.objects.all()
    count_results = {res.test_id: 0 for res in results}
    
    for res in results:
        count_results[res.test_id] += 1
    
    data = {test: [test, count_results[test.id] if StudentResponse.objects.filter(test_id=test.id).exists() else 0,
                Test.objects.filter(id=test.id)[0].questions.count()] for test in tests}    
    tmp_tests = Test.objects.exclude(tmp=False)
    
    return render(request, 'tests/tests_list_admin.html', {
                                'data': data,
                                'tmp_tests': tmp_tests
                            })


@login_required
def test_open_status_update(request, test_id, status=None):
    test = Test.objects.filter(id=test_id)
    if status==0:
        test.update(repeated_answer=0)
    else:
        test.update(repeated_answer=1)
    
    return test_list_admin(request)


@login_required
def add_test(request):
    if request.method == 'POST':
        test_form = TestForm(request.POST)
        if test_form.is_valid() and test_form.cleaned_data['title'] not in [test.title for test in Test.objects.all()]:
            test = test_form.save(commit=False)  # Не сохраняем еще в БД
            test.created_by = request.user  # Устанавливаем текущего пользователя
            test.save()  # Теперь сохраняем в БД
    else:
        test_form = TestForm()
    tmp_tests = Test.objects.exclude(tmp=False)
    
    return render(request, 'tests/add_test.html', {
                'test_form': test_form,
                'tmp_tests': tmp_tests
                })


@login_required
def edit_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)  # Получаем тест по ID

    if request.method == 'POST':
        test_form = TestForm(request.POST, instance=test)  # Передаем существующий объект в форму
        if test_form.is_valid():
            test_form.save()  # Сохраняем изменения
            # TODO: Добавляется и обновляется: ТОЛЬКО обновлять
            return test_list_admin(request)  # Перенаправление на страницу теста
    else:
        test_form = TestForm(instance=test)  # Загружаем данные в форму для редактирования

    return render(request, 'tests/edit_test.html', {'test_form': test_form, 'test': test})


@login_required
def delete_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    print(f'Тест "{test}" с ID: {test.id} удален.')
    if request.method == 'POST':
        test.delete()
        return add_test(request)
    
    return render(request, 'tests/delete_test.html', {'test': test})


@login_required
def add_question(request, test_id):
    if test_id != 0:
        test = get_object_or_404(Test, id=test_id)
        # Добавить галочку - создать тест без вопросов, добавить их познее
        if request.method == 'POST':
            question_form = QuestionForm(request.POST)
            if question_form.is_valid():
                hesh_quest = calculate_hash(question_form['question'])
                print(hesh_quest)
                question = question_form.save(commit=False)
                question.test = test  # Привязываем вопрос к тесту
                question.save()
                return redirect('edit_test', test_id=test_id)  # Перенаправление на страницу теста
        else:
            question_form = QuestionForm()

        return render(request, 'tests/add_question.html', {'question_form': question_form, 'test': test})
    else:
        if request.method == 'POST':
            question_form = QuestionForm(request.POST)
            if question_form.is_valid() and question_form.cleaned_data['text'] not in [quest.text for quest in Question.objects.all()]:
                # hesh_quest = calculate_hash(question_form.cleaned_data['text'])
                # print(hesh_quest)
                question = question_form.save(commit=False)
                question.save()
                return redirect('list_questions')  # Перенаправление на страницу теста
        else:
            question_form = QuestionForm()

        return render(request, 'tests/add_question.html', {'question_form': question_form})

@login_required
def questions_list_admin(request):
    questions = Question.objects.all() # Отбор всех вопросов в БД
    list_topics = list(questions.values_list('topics').distinct())
    
    return render(request, 'tests/questions_list_admin.html', {
                                'data': questions,
                                'topics': list_topics
                            })


@login_required
def edit_question(request, id):
    question = get_object_or_404(Question, id=id)  # Получаем вопрос по ID

    if request.method == 'POST':
        quest_form = QuestionForm(request.POST, instance=question)  # Передаем существующий объект в форму
        if quest_form.is_valid():
            quest_form.save()  # Сохраняем изменения
            # TODO: Добавляется и обновляется: ТОЛЬКО обновлять
            return questions_list_admin(request)  # Перенаправление на страницу теста
    else:
        quest_form = QuestionForm(instance=question)  # Загружаем данные в форму для редактирования

    return render(request, 'tests/edit_question.html', {'quest_form': quest_form, 'question': question})


@login_required
def delete_question(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == 'POST':
        question.delete()
        print(f'Вопрос "{question}" с ID: {question.id} удален.')
        return questions_list_admin(request)
    
    return render(request, 'tests/delete_question.html', {'question': question})

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
            answers_student = dict([(int(k.split('_')[-1]), v) for k, v in answers.items()])
            answers_correct_student_for_db = {k: answers_student[k]==answer_correct_db[k] for k, v in answers_student.items()}
            score = sum([int(v) for v in answers_correct_student_for_db.values()]) # Итог
            response.right_answer = answers_correct_student_for_db
            response.score = score
            response.save()
            return redirect('test_results', response.id)
    else:
        form = TestResponseForm(questions=test.questions.all())

    return render(request, 'tests/take_test.html', {
                                                    'test': test, 'form': form
                                                    })


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
        if request.user.is_superuser:
            results = StudentResponse.objects.all().distinct()
            print(set(results))
            return render(request, 'tests/my_tests.html', {'results': set(results)})
        else:
            results = StudentResponse.objects.filter(student_id=request.user.id)
            return render(request, 'tests/my_tests.html', {'results': results})
    else:
        return redirect('login') 


@login_required
def tests_all_results_admin(request):
    if request.user.is_superuser:
        results = StudentResponse.objects.all()
        tests = Test.objects.exclude(tmp=True)
        count_results = {res.test_id:0 for res in results}
        for res in results:
            count_results[res.test_id] += 1
        data = {test: [test, count_results[test.id] if StudentResponse.objects.filter(test_id=test.id).exists() else 0] for test in tests}
        return render(request, 'tests/tests_all_results_admin.html', {'data': data})
                    
    else:
        return redirect('login') 


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') 
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


def test_report(request):
    responses = StudentResponse.objects.all()  # Получаем все ответы студентов
    
    return render(request, 'admin/test_report.html', {'responses': responses})




# TODO: Проверка, если уже проходил и отключена повторная отправка - закрыть тест +++
# TODO: Отсечь тесты по классам: чужие тесты убрать из списка тестов +++
# TODO: WYSYWIG редактор тестов +++
# TODO: Отчет по тестированиям +++
# TODO: Доделать смену статуса теста - открыть/закрыть +++
# TODO: Собрать данные в таблицу: сколько сдано + ссылки на подробности по тестам +++
# TODO: Функционал создания, редактирования, удаления тестов +++ и вопросов, +++
                                                    # добавление готовых вопросов +++
# TODO: Проверка и отсечка добавления теста с уже существующим названием +++
# TODO: Проверка и отсечка добавления вопроса с уже существующим текстом +++
# TODO: Добавление картинок и файлов к вопросу (Сейчас - только ссылка на внешний ресурс) ---
# TODO: Вопрос со вставкой нескольких чисел (ЕГЭ 17, 18, 25, 26, 27) ---


# Не актуально:
# TODO: Генератор заданий на основе шаблонов (МЦКО-7,8,9,10, ЕГЭ-11) +--
# TODO: Добавить проверку вручную ответов для сложных заданий ---