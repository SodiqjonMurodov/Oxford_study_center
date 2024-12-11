from django.db import models
from phonenumber_field.formfields import PhoneNumberField
from rest_framework.exceptions import ValidationError
from common.models import BaseModel
from users.models import User


class Course(BaseModel):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='courses/', default='default/course.png')
    description = models.TextField(default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class CourseView(BaseModel):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='views')
    ip_address = models.GenericIPAddressField()

    class Meta:
        unique_together = ('course', 'ip_address')
        verbose_name = 'Course View'
        verbose_name_plural = 'Course Views'

    def __str__(self):
        return f"{self.ip_address} viewed {self.course.name}"


class Review(BaseModel):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


class ReviewLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    review = models.ForeignKey('Review', on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f'{self.id}'

    class Meta:
        unique_together = ('user', 'review')
        verbose_name = 'Review Like'
        verbose_name_plural = 'Review Likes'


class Rating(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

    def validate(self):
        if not self.rating == [0, 1, 2, 3, 4, 5]:
            raise ValidationError('Rating must be between 0 and 5')


class Feedback(BaseModel):
    fullname = models.CharField(max_length=150)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    phone_number = PhoneNumberField()
    message = models.TextField()

    def __str__(self):
        return f'{self.fullname}'

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'


