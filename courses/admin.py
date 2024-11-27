from django.contrib import admin
from courses.models import Course, Rating, Review

admin.site.register(Course)
admin.site.register(Rating)
admin.site.register(Review)
