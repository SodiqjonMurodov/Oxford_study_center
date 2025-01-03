from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from pip._vendor.chardet.metadata.languages import Language
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from common.utils import send_confirmation_email, check_email, check_phone_number
from .models import User, UserConfirmation, CODE_VERIFIED, DONE, NEW


class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'auth_status'
        )
        extra_kwargs = {
            'auth_status': {'read_only': True, 'required': False}
        }

    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)
        code = user.create_verify_code()
        send_confirmation_email(user.email, code)
        user.save()
        return user

    def validate_email(self, value):
        email = value.lower()
        if value and User.objects.filter(email=value).exists():
            data = {
                "success": False,
                "message": "This email already exists in the database"
            }
            raise ValidationError(data)
        else:
            check_email(email)
            return email

    def to_representation(self, instance):
        data = super(SignUpSerializer, self).to_representation(instance)
        data.update(instance.token())
        return data


class ChangeUserInformation(serializers.Serializer):
    fullname = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError(
                {
                    "success": False,
                    "message": "Your password values do not match"
                }
            )
        validate_password(password)
        return data

    def update(self, instance, validated_data):
        instance.fullname = validated_data.get('fullname', instance.fullname)

        if validated_data.get('password'):
            instance.set_password(validated_data['password'])

        if hasattr(instance, 'auth_status') and instance.auth_status == CODE_VERIFIED:
            instance.auth_status = DONE

        instance.save()
        return instance


class LoginSerializer(TokenObtainPairSerializer):
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

        current_user = User.objects.filter(email__iexact=email).first()

        if current_user is not None and current_user.auth_status in [NEW, CODE_VERIFIED]:
            raise ValidationError(
                {
                    'success': False,
                    'message': "You are not fully registered!",
                    'auth_status': current_user.auth_status
                }
            )

        data = super().validate(attrs)
        data['user_id'] = user.id
        return data


class LoginRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        access_token_instance = AccessToken(data['access'])
        user_id = access_token_instance['user_id']
        user = get_object_or_404(User, id=user_id)
        update_last_login(None, user)
        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get('email', None)
        if email is None:
            raise ValidationError(
                {
                    "success": False,
                    'message': "Email is required!"
                }
            )
        user = User.objects.filter(email=email)
        if not user.exists():
            raise NotFound(detail="User not found")
        attrs['user'] = user.first()
        return attrs


class ResetPasswordSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(min_length=8, required=True, write_only=True)
    confirm_password = serializers.CharField(min_length=8, required=True, write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'password',
            'confirm_password'
        )

    def validate(self, data):
        password = data.get('password', None)
        confirm_password = data.get('password', None)
        if password != confirm_password:
            raise ValidationError(
                {
                    'success': False,
                    'message': "Parollaringiz qiymati bir-biriga teng emas"
                }
            )
        if password:
            validate_password(password)
        return data

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        instance.set_password(password)
        return super(ResetPasswordSerializer, self).update(instance, validated_data)


class UserLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['language']
