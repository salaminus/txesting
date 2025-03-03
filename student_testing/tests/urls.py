from django.urls import path
from .views import test_list, take_test, test_results, \
                        test_students_results, home, user_test_results, \
                        register, login_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', home, name='home'),
    path('tests_list', test_list, name='test_list'),
    path('take/<int:test_id>/', take_test, name='take_test'),
    path('results/<int:response_id>/', test_results, name='test_results'),
    # path('test-results/<int:test_id>', test_results, name='test_results'),
    path('test_students_results/<int:test_id>', test_students_results, name='test_students_results'),
    path('my_tests/', user_test_results, name='my_tests'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

