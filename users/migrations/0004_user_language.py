# Generated by Django 5.1.2 on 2025-01-03 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_user_gender_en_remove_user_gender_ru_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='language',
            field=models.CharField(choices=[('UZ', 'Uzbek'), ('RU', 'Russian'), ('EN', 'English')], default='UZ', max_length=10, verbose_name='language'),
        ),
    ]
