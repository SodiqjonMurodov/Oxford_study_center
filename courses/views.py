from django.db.models import Avg
from django.db.models.functions import Round
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Course, Review, Rating
from .serializers import CourseDetailSerializer, CourseListSerializer, \
    ReviewCreateUpdateSerializer, RatingCreateSerializer, RatingUpdateSerializer, ReviewLikeUpdateSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication



class CourseListAPIView(ListAPIView):
    serializer_class = CourseListSerializer

    def get_queryset(self):
        return Course.objects.annotate(
            average_rating=Round(Avg('rating__rating') * 10) / 10
        )


class CourseDetailAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Course.objects.annotate(
            average_rating=Round(Avg('rating__rating') * 10) / 10
        )
    

class ReviewCreateAPIView(CreateAPIView):
    serializer_class = ReviewCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class ReviewUpdateAPIView(UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)
    

class ReviewLikeUpdateAPIView(UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewLikeUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)


class ReviewDeleteAPIView(DestroyAPIView):
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response(
            {"detail": "Review deleted successfully."},
            status=status.HTTP_200_OK
        )

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)


class RatingCreateAPIView(CreateAPIView):
    serializer_class = RatingCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class RatingUpdateAPIView(UpdateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
