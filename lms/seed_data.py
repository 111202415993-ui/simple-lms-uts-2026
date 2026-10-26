
from django.db import transaction
from lms.models import Lecturer, Course, Student, Lesson, Enrollment, Assignment, Submission


@transaction.atomic
def seed_data():
    # Buat dosen
    lecturer, _ = Lecturer.objects.get_or_create(
        email="dosen@example.com",
        defaults={"name": "Dosen Pengujian"}
    )

    # Buat minimal 10.000 Course
    batch_size = 1000
    total_courses = 10000

    for start in range(0, total_courses, batch_size):
        courses = [
            Course(
                title=f"Course Pemrograman {i}",
                code=f"CRS{i:05d}",
                lecturer=lecturer,
                description=f"Deskripsi course {i}"
            )
            for i in range(start + 1, start + batch_size + 1)
        ]

        Course.objects.bulk_create(courses, batch_size=batch_size)

    # Buat beberapa lesson untuk pengujian prefetch_related
    all_courses = Course.objects.order_by("id")

    lessons = []
    for course in all_courses.iterator(chunk_size=1000):
        lessons.append(
            Lesson(
                course=course,
                title=f"Materi 1 - {course.title}",
                content="Materi pembelajaran"
            )
        )

    Lesson.objects.bulk_create(lessons, batch_size=1000)

    print("Data pengujian berhasil dibuat.")
    print(f"Jumlah Course: {Course.objects.count()}")
    print(f"Jumlah Lecturer: {Lecturer.objects.count()}")
    print(f"Jumlah Lesson: {Lesson.objects.count()}")
