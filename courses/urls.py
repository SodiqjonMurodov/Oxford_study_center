from django.urls import path
from .views import CourseDetailAPIView, CourseListAPIView, ReviewCreateAPIView, ReviewDeleteAPIView,\
    RatingCreateAPIView, RatingUpdateAPIView, ReviewUpdateAPIView, ReviewLikeUpdateAPIView

urlpatterns = [
    # Course Endpoints
    path('courses/', CourseListAPIView.as_view(), name='courses'),
    path('courses/<slug:pk>', CourseDetailAPIView.as_view(), name='course-detail'),
    # Review Endpoints
    path('review/create/', ReviewCreateAPIView.as_view(), name='review-create'),
    path('review/update/<slug:pk>', ReviewUpdateAPIView.as_view(), name='review-update'),
    path('review/delete/<slug:pk>', ReviewDeleteAPIView.as_view(), name='review-delete'),
    path('review/like/update/<slug:pk>', ReviewLikeUpdateAPIView.as_view(), name='review-like-update'),
    # Rating Endpoints
    path('rating/create/', RatingCreateAPIView.as_view(), name='rating-create'),
    path('rating/update/<slug:pk>', RatingUpdateAPIView.as_view(), name='rating-update'),
]