import random
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now, timedelta

from common.models import BaseModel

MALE, FEMALE = ('male', 'female')
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
    GENDER_CHOICES = (
        (MALE, MALE),
        (FEMALE, FEMALE),
    )
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=150, blank=True, null=True)
    lastname = models.CharField(max_length=150, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    @property
    def full_name(self):
        return f'{self.firstname} {self.lastname}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def create_verify_code(self):
        code = "".join([str(random.randint(0, 100) % 10) for _ in range(4)])
        while UserConfirmation.objects.filter(code=code).exists():
            code = "".join([str(random.randint(0, 100) % 10) for _ in range(4)])
        UserConfirmation.objects.create(
            user_id=self.pk,
            code=code
        )
        return code


class UserConfirmation(BaseModel):
    code = models.CharField(max_length=4, unique=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    expiration_time = models.DateTimeField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = _('User Confirmation')
        verbose_name_plural = _('User Confirmations')

    def save(self, *args, **kwargs):
        if not self.pk or self.is_confirmed == False:
            self.expiration_time = now() + timedelta(minutes=EMAIL_EXPIRE_TIME)
        super(UserConfirmation, self).save(*args, **kwargs)


