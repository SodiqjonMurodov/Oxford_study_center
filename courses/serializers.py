from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from common.utils import check_phone_number
from courses.models import Course, Review, Rating, Feedback, ReviewLike
from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class CourseListSerializer(ModelSerializer):
    rating = serializers.FloatField(source='average_rating', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'rating', 'image']


class CourseDetailSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(source='average_rating', read_only=True)
    reviews = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'rating', 'image', 'description', 'views', 'reviews']

    def get_reviews(self, obj):
        request = self.context.get('request')
        reviews = obj.reviews.all()
        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 15
        paginated_reviews = paginator.paginate_queryset(reviews, request)

        return paginator.get_paginated_response(
            ReviewSerializer(paginated_reviews, many=True, context={'request': request}).data
        ).data

    def get_views(self, obj):
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
            return obj.likes.filter(user=user, like=True).exists()
        return False


class ReviewCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'course', 'comment', 'parent', 'author']


class ReviewLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewLike
        fields = ['id', 'user', 'review', 'like', 'created_at']


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
    course = CourseListSerializer(required=True)
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = Feedback
        fields = ['id', 'fullname', 'course', 'phone_number', 'message']

    def validate(self, attrs):
        phone = attrs.get('phone_number')
        check_phone_number(phone)
        return attrs




