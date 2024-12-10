from django.contrib import admin
from django.utils.html import format_html
from courses.models import Course, Rating, Review, CourseView


@admin.register(Course)
class CourseModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image_tag']

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 35px;" />', obj.image.url)
        return "No Image"

    image_tag.short_description = "Image"


@admin.register(Rating)
class RatingModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'user', 'rating']


@admin.register(Review)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'author', 'parent', 'comment']
