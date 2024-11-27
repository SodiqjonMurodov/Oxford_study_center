from django.db.models import Avg
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Course
from .serializers import CourseCreateSerializer, CourseDetailSerializer, CourseListSerializer


class CourseCreateAPIView(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer
    permission_classes = [IsAuthenticated]



class CourseListAPIView(ListAPIView):
    serializer_class = CourseListSerializer

    def get_queryset(self):
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



class CourseDetailAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
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

