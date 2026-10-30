from django.contrib import admin
from django.urls import path
from lms.views import course_list_baseline, course_list_prefetch, course_list_optimized

urlpatterns = [
    path('admin/', admin.site.urls),
    path('baseline/', course_list_baseline, name='course_list_baseline'),
    path('prefetch/', course_list_prefetch, name='course_list_prefetch'),
    path('optimized/', course_list_optimized, name='course_list_optimized'),
]