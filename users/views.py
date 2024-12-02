from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import SignUpSerializer, UserProfileSerializer, \
    EmailTokenObtainPairSerializer, EmailTokenRefreshSerializer
from users.models import User


class CreateUserAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]


class CompleteUserProfileAPIView(UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

class EmailTokenRefreshView(TokenRefreshView):
    serializer_class = EmailTokenRefreshSerializer



