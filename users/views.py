from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import SignUpSerializer, CreateUserProfileSerializer
from users.models import User


class CreateUserAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(is_active=False)


class CompleteUserProfileAPIView(UpdateAPIView):
    serializer_class = CreateUserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Ensure the authenticated user is the one being updated
        return self.request.user

    def perform_update(self, serializer):
        # Ensure `is_active` is set to True during profile completion
        serializer.save(is_active=True)


