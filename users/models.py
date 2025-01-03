import random
import uuid
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now, timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from phonenumber_field.modelfields import PhoneNumberField
from common.models import BaseModel

NEW, CODE_VERIFIED, DONE, PHOTO_DONE = ('new', 'code_verified', 'done', 'photo_done')
EMAIL_EXPIRE_TIME = 2


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email field is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    AUTH_STATUS = (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
        (DONE, DONE),
    )
    GENDER_CHOICES = (
        ('MALE', _('Male')),
        ('FEMALE', _('Female')),
    )
    LANGUAGE_CHOICES = (
        ('uz', _('Uzbek')),
        ('ru', _('Russian')),
        ('en', _('English')),
    )
    email = models.EmailField(_('email'), unique=True)
    auth_status = models.CharField(_('auth status'), max_length=31, choices=AUTH_STATUS, default=NEW)
    fullname = models.CharField(_('fullname'), max_length=150, blank=True, null=True)
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    gender = models.CharField(_('gender'), max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    phone_number = PhoneNumberField(_('phone number'), null=True, blank=True)
    language = models.CharField(_('language'), max_length=10, choices=LANGUAGE_CHOICES, default='ru')
    is_active = models.BooleanField(_('is active'), default=True)
    is_staff = models.BooleanField(_('login to the admin panel'), default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def create_verify_code(self):
        code = "".join([str(random.randint(0, 100) % 10) for _ in range(4)])
        user_codes = UserConfirmation.objects.filter(code=code)
        experition_times = user_codes.filter(expiration_time__gte=now())
        while user_codes.exists() and experition_times.exists():
            code = "".join([str(random.randint(0, 100) % 10) for _ in range(4)])
        UserConfirmation.objects.create(
            user_id=self.pk,
            code=code
        )
        return code

    def check_email(self):
        if self.email:
            normalize_email = self.email.lower()
            self.email = normalize_email

    def check_pass(self):
        if not self.password:
            temp_password = f'password-{uuid.uuid4().__str__().split("-")[-1]}'
            self.password = temp_password

    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh_token": str(refresh)
        }

    def save(self, *args, **kwargs):
        self.clean()
        super(User, self).save(*args, **kwargs)

    def clean(self):
        self.check_email()
        self.check_pass()
        self.hashing_password()


class UserConfirmation(BaseModel):
    code = models.CharField(_('code'), max_length=4)
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE, related_name='verify_codes',
                             verbose_name=_('user'))
    expiration_time = models.DateTimeField(_('expiration time'), null=True, blank=True)
    is_confirmed = models.BooleanField(_('is confirmed'), default=False)

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = _('User Confirmation')
        verbose_name_plural = _('User Confirmations')

    def save(self, *args, **kwargs):
        if not self.pk or self.is_confirmed == False:
            self.expiration_time = now() + timedelta(minutes=EMAIL_EXPIRE_TIME)
        super(UserConfirmation, self).save(*args, **kwargs)
