from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer
from django.core.validators import validate_email
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import serializers
from common.utils import send_confirmation_email
from .models import User, UserConfirmation


class SignUpSerializer(ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm']

    def validate_email(self, value):
        try:
            validate_email(value)
        except serializers.ValidationError:
            raise serializers.ValidationError("Invalid email format.")

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")

        return value

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        validate_password(data['password'])
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = super(SignUpSerializer, self).create(validated_data)
        try:
            # Create code to user confirmation
            code = user.create_verify_code()
            mess = send_confirmation_email(user.email, code)
            user.save()
            return user
        except Exception:
            raise serializers.ValidationError("Email confirmation failed.")


class UserConfirmationSerializer(ModelSerializer):
    class Meta:
        model = UserConfirmation
        fields = ['email', 'code']

    def validate(self):
        user_confirmation = UserConfirmation.objects.filter(code=self.validated_data['code'])






class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'phone_number']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'date_of_birth': {'required': True},
            'gender': {'required': True},
            'phone_number': {'required': True},
        }


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")

        data = super().validate(attrs)
        return data


class EmailTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = attrs.get("refresh")

        if not refresh:
            raise serializers.ValidationError({"refresh": "This field is required."})

        try:
            token = RefreshToken(refresh)
            data = {"access": str(token.access_token)}

            # Optionally include additional user information in the response
            if api_settings.UPDATE_LAST_LOGIN:
                user = token.user
                data["email"] = user.email  # Include the user's email in the response

            return data
        except Exception as e:
            raise serializers.ValidationError({"refresh": "Invalid refresh token."})
