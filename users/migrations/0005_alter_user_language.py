# Generated by Django 5.1.2 on 2025-01-03 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(choices=[('uz', 'Uzbek'), ('ru', 'Russian'), ('en', 'English')], default='UZ', max_length=10, verbose_name='language'),
        ),
    ]
