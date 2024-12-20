# Generated by Django 5.1.2 on 2024-12-10 15:45

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='status',
        ),
        migrations.AlterField(
            model_name='review',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='courses.course'),
        ),
        migrations.CreateModel(
            name='CourseView',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='courses.course')),
            ],
            options={
                'unique_together': {('course', 'ip_address')},
            },
        ),
    ]
