from django.http import JsonResponse
from django.db import connection
from django.db import reset_queries
from django.test.utils import CaptureQueriesContext
from .models import Course


def course_list_baseline(request):
    with CaptureQueriesContext(connection) as queries:
        courses = Course.objects.select_related('lecturer').all()[:100]

        data = []
        for course in courses:
            data.append({
                "title": course.title,
                "lecturer": course.lecturer.name,
            })

    return JsonResponse({
        "total_courses": len(data),
        "total_queries": len(queries),
        "data": data,
    })


def course_list_prefetch(request):
    with CaptureQueriesContext(connection) as queries:
        courses = Course.objects.prefetch_related('lessons').all()[:100]

        data = []

        for course in courses:
            data.append({
                "title": course.title,
                "lessons": [
                    lesson.title for lesson in course.lessons.all()
                ]
            })

    return JsonResponse({
        "total_courses": len(data),
        "total_queries": len(queries),
        "data": data,
    })
def course_list_optimized(request):
    with CaptureQueriesContext(connection) as queries:
        courses = Course.objects.select_related('lecturer').all()[:100]

        data = []
        for course in courses:
            data.append({
                "title": course.title,
                "lecturer": course.lecturer.name,
            })

    return JsonResponse({
        "total_courses": len(data),
        "total_queries": len(queries),
        "data": data,
    })