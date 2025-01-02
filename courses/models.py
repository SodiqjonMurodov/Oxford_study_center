from django.db import models
from rest_framework.exceptions import ValidationError
from common.models import BaseModel
from users.models import User
from django.utils.translation import gettext_lazy as _


class Course(BaseModel):
    name = models.CharField(_('name'), max_length=100)
    image = models.ImageField(_('image'), upload_to='courses/', default='default/course.png')
    description = models.TextField(_('description'), default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')


class CourseView(BaseModel):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='views', verbose_name=_('course'))
    ip_address = models.GenericIPAddressField(verbose_name=_('IP address'))

    class Meta:
        unique_together = ('course', 'ip_address')
        verbose_name = _('Course View')
        verbose_name_plural = _('Course Views')

    def __str__(self):
        return f"{self.ip_address} viewed {self.course.name}"


class Review(BaseModel):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='reviews', verbose_name=_('course'))
    comment = models.TextField(_('comment'), )
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name=_('receiver'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('author'))

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')


class ReviewLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes", verbose_name=_('user'))
    review = models.ForeignKey('Review', on_delete=models.CASCADE, related_name="likes", verbose_name=_('review'))

    def __str__(self):
        return f'{self.id}'

    class Meta:
        unique_together = ('user', 'review')
        verbose_name = _('Review Like')
        verbose_name_plural = _('Review Likes')


class Rating(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="grades", verbose_name=_('course'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    rating = models.PositiveIntegerField(_('rating'), default=0)

    class Meta:
        verbose_name = _('Rating')
        verbose_name_plural = _('Ratings')

    def validate(self):
        if not self.rating == [0, 1, 2, 3, 4, 5]:
            raise ValidationError('Rating must be between 0 and 5')


class Feedback(BaseModel):
    fullname = models.CharField(_('fullname'), max_length=150)
    age = models.IntegerField(_('age'), blank=True, null=True)
    email = models.EmailField(_('email'), blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="feedbacks", verbose_name=_('course'))
    phone_number = models.CharField(_('phone number'), max_length=15)
    message = models.TextField(_('message'), )

    def __str__(self):
        return f'{self.fullname}'

    class Meta:
        verbose_name = _('Feedback')
        verbose_name_plural = _('Feedbacks')


