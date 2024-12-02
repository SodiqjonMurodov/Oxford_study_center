from django.urls import path
from .views import CreateUserAPIView, CompleteUserProfileAPIView, EmailTokenObtainPairView, EmailTokenRefreshView

urlpatterns = [
    path('signup/', CreateUserAPIView.as_view(), name='signup'),
    path('signup/create-profile/', CompleteUserProfileAPIView.as_view(), name='create_profile'),
    path('token/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', EmailTokenRefreshView.as_view(), name='token_refresh'),
]
