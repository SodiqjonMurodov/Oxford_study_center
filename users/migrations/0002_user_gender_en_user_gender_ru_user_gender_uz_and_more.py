# Generated by Django 5.1.2 on 2025-01-02 15:31

import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender_en',
            field=models.CharField(blank=True, choices=[('MALE', 'Male'), ('FEMALE', 'Female')], max_length=6, null=True, verbose_name='gender'),
        ),
        migrations.AddField(
            model_name='user',
            name='gender_ru',
            field=models.CharField(blank=True, choices=[('MALE', 'Male'), ('FEMALE', 'Female')], max_length=6, null=True, verbose_name='gender'),
        ),
        migrations.AddField(
            model_name='user',
            name='gender_uz',
            field=models.CharField(blank=True, choices=[('MALE', 'Male'), ('FEMALE', 'Female')], max_length=6, null=True, verbose_name='gender'),
        ),
        migrations.AlterField(
            model_name='user',
            name='auth_status',
            field=models.CharField(choices=[('new', 'new'), ('code_verified', 'code_verified'), ('done', 'done')], default='new', max_length=31, verbose_name='auth status'),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='date of birth'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='user',
            name='fullname',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='fullname'),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('MALE', 'Male'), ('FEMALE', 'Female')], max_length=6, null=True, verbose_name='gender'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is active'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='login to the admin panel'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='phone number'),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated at'),
        ),
        migrations.AlterField(
            model_name='userconfirmation',
            name='code',
            field=models.CharField(max_length=4, verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='userconfirmation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='userconfirmation',
            name='expiration_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='expiration time'),
        ),
        migrations.AlterField(
            model_name='userconfirmation',
            name='is_confirmed',
            field=models.BooleanField(default=False, verbose_name='is confirmed'),
        ),
        migrations.AlterField(
            model_name='userconfirmation',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated at'),
        ),
        migrations.AlterField(
            model_name='userconfirmation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verify_codes', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]