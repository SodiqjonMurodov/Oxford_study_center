from django.urls import path
from .views import CreateUserAPIView, CompleteUserProfileAPIView

urlpatterns = [
    path('signup/', CreateUserAPIView.as_view(), name='signup'),
    path('signup/create-profile/', CompleteUserProfileAPIView.as_view(), name='create_profile'),
]
