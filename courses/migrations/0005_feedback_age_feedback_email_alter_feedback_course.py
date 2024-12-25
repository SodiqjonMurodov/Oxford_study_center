# Generated by Django 5.1.2 on 2024-12-25 15:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_courseview_options_alter_rating_course_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='feedback',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='courses.course'),
        ),
    ]
