from .models import Course
from django.db.models import Avg


def save_rating_and_status():
    courses = Course.objects.annotate(average_rating=Avg('rating__rating'))
    for course in courses:
        if course.average_rating is not None:
            if course.average_rating >= 4.5:
                course.status = 'Excellent'
            elif course.average_rating >= 3.5:
                course.status = 'Good'
            elif course.average_rating >= 2.5:
                course.status = 'Normal'
            elif course.average_rating >= 1.5:
                course.status = 'Bad'
            else:
                course.status = 'Terrible'
            course.save()
    return courses