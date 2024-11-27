from django.urls import path
from .views import CourseCreateAPIView, CourseDetailAPIView, CourseListAPIView

urlpatterns = [
    path('courses/', CourseListAPIView.as_view(), name='courses'),
    path('courses/<slug:pk>', CourseDetailAPIView.as_view(), name='course-detail'),
    path('courses/create/', CourseCreateAPIView.as_view(), name='courses'),
]