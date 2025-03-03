from django.contrib import admin
from django.urls import path, include
from tests.views import test_list, test_results, test_students_results


urlpatterns = [
    path('admin/', admin.site.urls),
    path('tests/', include('tests.urls')),
    path('', include('tests.urls')),
]
