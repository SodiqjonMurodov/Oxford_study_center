from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from common.utils import check_phone_number, check_email
from courses.models import Course, Review, Rating, Feedback, ReviewLike
from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class CourseListSerializer(ModelSerializer):
    rating = serializers.FloatField(source='average_rating', read_only=True)
    grades_count = serializers.SerializerMethodField()
    views_count = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'rating', 'image', 'description', 'grades_count', 'views_count', 'reviews_count']

    def get_grades_count(self, obj):
        return obj.grades.count()

    def get_reviews_count(self, obj):
        return obj.reviews.count()

    def get_views_count(self, obj):
        return obj.views.count()


class CourseDetailSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(source='average_rating', read_only=True)
    grades_count = serializers.SerializerMethodField()
    views_count = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'rating', 'image', 'description', 'grades_count', 'views_count', 'reviews_count', 'reviews']

    def get_reviews(self, obj):
        request = self.context.get('request')
        reviews = obj.reviews.all()
        # Paginator
        paginator = PageNumberPagination()
        paginator.page_size = 15
        paginated_reviews = paginator.paginate_queryset(reviews, request)

        return paginator.get_paginated_response(
            ReviewSerializer(paginated_reviews, many=True, context={'request': request}).data
        ).data
    
    def get_grades_count(self, obj):
        return obj.grades.count()
    
    def get_reviews_count(self, obj):
        return obj.reviews.count()

    def get_views_count(self, obj):
        return obj.views.count()


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_user_liked = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'comment', 'parent', 'author', 'is_author', 'likes_count', 'is_user_liked', 'created_at', 'updated_at']

    def get_author(self, obj):
        return UserSerializer(obj.author).data
    
    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_author(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.author == request.user
        return False
    
    def get_is_user_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.likes.filter(user=user).exists()
        return False


class ReviewCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'course', 'comment', 'parent', 'author']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'course', 'user', 'rating']
        read_only_fields = ['user']

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        course = attrs.get('course')
        if self.instance is None and Rating.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError("You have already rated this course.")
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class FeedbackSerializer(ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'fullname', 'age', 'email', 'course', 'phone_number', 'message']

    def validate_course(self, value):
        if not Course.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Invalid course ID provided.")
        return value

    def validate(self, attrs):
        email = attrs.get('email')
        check_email(email)
        phone = attrs.get('phone_number')
        check_phone_number(phone)
        return attrs




