from django.urls import path
from .views import CourseDetailAPIView, CourseListAPIView, ReviewCreateAPIView, ReviewDeleteAPIView,\
    RatingAPIView, ReviewUpdateAPIView, FeedbackFormCreateAPIView, ReviewLikeToggleView

urlpatterns = [
    path('courses/', CourseListAPIView.as_view(), name='courses'),
    path('courses/<slug:pk>', CourseDetailAPIView.as_view(), name='course-detail'),

    path('review/create/', ReviewCreateAPIView.as_view(), name='review-create'),
    path('review/update/<uuid:pk>/', ReviewUpdateAPIView.as_view(), name='review-update'),
    path('review/delete/<uuid:pk>/', ReviewDeleteAPIView.as_view(), name='review-delete'),
    path('review/<slug:comment_id>/like/', ReviewLikeToggleView.as_view(), name='review-like'),

    path('rating/', RatingAPIView.as_view(), name='rating'),
    path('contact-form/', FeedbackFormCreateAPIView.as_view(), name='feedback'),
]
