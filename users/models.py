import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

MALE, FEMALE = ('male', 'female')

class User(AbstractUser):
    GENDER_CHOICES = (
        (MALE, MALE),
        (FEMALE, FEMALE),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

