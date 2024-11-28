from django.db import models
from rest_framework.exceptions import ValidationError
from common.models import BaseModel
from users.models import User

NONE, TERRIBLE, BAD, NORMAL, GOOD, EXCELLENT = ("None", "Terrible", "Bad", "Normal", "Good", "Excellent")

class Course(BaseModel):
    STATUS_CHOICES = (
        (NONE, NONE),
        (TERRIBLE, TERRIBLE),
        (BAD, BAD),
        (NORMAL, NORMAL),
        (GOOD, GOOD),
        (EXCELLENT, EXCELLENT)
    )
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='courses/', default='default/course.png')
    description = models.TextField(default='')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=NONE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class Review(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    comment = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


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

