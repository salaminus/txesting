from django.urls import path
from .views import test_list, take_test, test_results, \
                        test_students_results, home, user_test_results, \
                        register, login_view, test_report, test_list_admin, add_test, \
                        test_open_status_update, tests_all_results_admin, \
                        add_question, edit_test, delete_test, questions_list_admin, \
                        edit_question, delete_question
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', home, name='home'),
    path('tests_list', test_list, name='test_list'),
    path('tests_list_admin', test_list_admin, name='tests_list_admin'),
    path('test_open_status_update/<int:test_id>', test_open_status_update, name='test_open_status_update'),
    path('test_open_status_update/<int:test_id>/status/<int:status>', test_open_status_update, name='test_open_status_update'),
    path('add_test/', add_test, name='add_test'),
    path('delete_test/<int:test_id>', delete_test, name='delete_test'),
    path('edit_test/<int:test_id>', edit_test, name='edit_test'),
    path('add_question/<int:test_id>', add_question, name='add_question'),
    path('list_questions/', questions_list_admin, name='list_questions'),
    path('delete_question/<int:id>', delete_question, name='delete_question'),
    path('edit_question/<int:id>', edit_question, name='edit_question'),
    path('take/<int:test_id>/', take_test, name='take_test'),
    path('results/<int:response_id>/', test_results, name='test_results'),
    path('test_students_results/<int:test_id>', test_students_results, name='test_students_results'),
    path('my_tests/', user_test_results, name='my_tests'),
    path('tests_all_results_admin/', tests_all_results_admin, name='tests_all_results_admin'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/test-report/', test_report, name='test_report'),
]

