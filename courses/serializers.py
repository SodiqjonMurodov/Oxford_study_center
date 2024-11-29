from django.db.models import Avg
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from courses.models import Course, Review, Rating
from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']


class CourseCreateSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'image', 'description']


class CourseListSerializer(ModelSerializer):
    rating = serializers.FloatField(source='average_rating', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'rating', 'status', 'image']


class CourseDetailSerializer(ModelSerializer):
    rating = serializers.FloatField(source='average_rating', read_only=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'rating', 'status', 'image', 'description', 'reviews']

    def get_reviews(self, obj):
        request = self.context.get('request')
        reviews = obj.review_set.all()

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_reviews = paginator.paginate_queryset(reviews, request)

        return paginator.get_paginated_response(
            ReviewSerializer(paginated_reviews, many=True, context={'request': request}).data
        ).data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'comment', 'parent', 'author', 'is_author', 'created_at', 'updated_at']

    def get_author(self, obj):
        return UserSerializer(obj.author).data

    def get_is_author(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.author == request.user
        return False


class ReviewCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'course', 'comment', 'parent', 'author']


class RatingCreateSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'course', 'user', 'rating']

    def validate(self, attrs):
        user = attrs.get('user')
        course = attrs.get('course')
        if Rating.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError("You have already rated this course.")
        return attrs


class RatingUpdateSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'course', 'user', 'rating']
