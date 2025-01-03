from django.urls import path
from .views import CreateUserAPIView, VerifyAPIView, GetNewVerification, ChangeUserInformationView, \
    LoginView, LoginRefreshView, LogOutView, ForgotPasswordView, ResetPasswordView, UserLanguageView

urlpatterns = [
    path('signup/', CreateUserAPIView.as_view(), name='signup'),
    path('verify/', VerifyAPIView.as_view()),
    path('new-verify/', GetNewVerification.as_view()),
    path('change-user/', ChangeUserInformationView.as_view()),
    path('lang/', UserLanguageView.as_view(), name='language'),

    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', LoginRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogOutView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
]
