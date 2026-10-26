
from django.test import TestCase
from django.db import connection
from django.test.utils import CaptureQueriesContext

from .models import Lecturer, Course, Lesson


class DatabaseOptimizationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.lecturer = Lecturer.objects.create(
            name="Dosen Test",
            email="dosen.test@example.com",
        )

        for i in range(3):
            course = Course.objects.create(
                title=f"Test Course {i}",
                code=f"TEST{i:03d}",
                lecturer=cls.lecturer,
                description="Course untuk pengujian",
            )

            Lesson.objects.create(
                course=course,
                title=f"Lesson {i}",
                content="Materi pengujian",
            )

    def test_select_related_uses_one_query(self):
        with self.assertNumQueries(1):
            courses = list(
                Course.objects.select_related("lecturer")
            )
            for course in courses:
                _ = course.lecturer.name

    def test_prefetch_related_uses_two_queries(self):
        with self.assertNumQueries(2):
            courses = list(
                Course.objects.prefetch_related("lessons")
            )
            for course in courses:
                list(course.lessons.all())

    def test_course_and_lesson_data_exist(self):
        self.assertEqual(Course.objects.count(), 3)
        self.assertEqual(Lesson.objects.count(), 3)
