from django.db.models import Avg
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from courses.models import Course, Review, Rating
from users.models import User


class CourseCreateSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'image', 'description']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']


class CourseListSerializer(ModelSerializer):
    rating = serializers.FloatField(source='average_rating', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'rating', 'status', 'image']


class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'comment', 'parent', 'author', 'created_at', 'updated_at']


class CourseDetailSerializer(ModelSerializer):
    rating = serializers.FloatField(source='average_rating', read_only=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'rating', 'status', 'image', 'description', 'reviews']

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        return ReviewSerializer(reviews, many=True).data
    

class ReviewCreateSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'course', 'comment', 'parent', 'author']


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'course', 'author', 'rating']
    






