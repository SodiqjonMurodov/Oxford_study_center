from django.urls import path
from .views import CourseCreateAPIView, CourseDetailAPIView, CourseListAPIView, ReviewCreateAPIView, ReviewDeleteAPIView,\
    RatingCreateAPIView, RatingUpdateAPIView, RatingDeleteAPIView

urlpatterns = [
    path('courses/', CourseListAPIView.as_view(), name='courses'),
    path('courses/<slug:pk>', CourseDetailAPIView.as_view(), name='course-detail'),
    path('courses/create/', CourseCreateAPIView.as_view(), name='course-create'),
    path('review/create/', ReviewCreateAPIView.as_view(), name='review-create'),
    path('review/delete/', ReviewDeleteAPIView.as_view(), name='review-delete'),
    path('rating/create/', RatingCreateAPIView.as_view(), name='rating-create'),
    path('rating/update/<slug:pk>', RatingUpdateAPIView.as_view(), name='rating-update'),
    path('rating/delete/<slug:pk>', RatingDeleteAPIView.as_view(), name='rating-delete'),
]