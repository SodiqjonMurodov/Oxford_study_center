from django.urls import path
from .views import CreateUserAPIView, CompleteUserProfileAPIView, EmailTokenObtainPairView, EmailTokenRefreshView, CheckEmail

urlpatterns = [
    path('signup/', CreateUserAPIView.as_view(), name='signup'),
    path('signup/create-profile/', CompleteUserProfileAPIView.as_view(), name='create_profile'),
    path('token/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', EmailTokenRefreshView.as_view(), name='token_refresh'),

    # Needing API's
    path('email/', CheckEmail.as_view(), name='check-email'),
    path('email/confirm/', CreateUserAPIView.as_view(), name='confirm-email'),
    path('email/confirm/signup/', CreateUserAPIView.as_view(), name='signup'),

]
