from django.db.models import Avg
from django.db.models.functions import Round
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from common.utils import get_client_ip
from .models import Course, Review, Rating, CourseView, ReviewLike, Feedback
from .serializers import CourseDetailSerializer, CourseListSerializer, \
    ReviewCreateUpdateSerializer, RatingSerializer, FeedbackSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


class CourseListAPIView(ListAPIView):
    serializer_class = CourseListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Course.objects.annotate(
            average_rating=Round(Avg('grades__rating') * 10) / 10
        )


class CourseDetailAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        course = self.get_object()
        ip_address = get_client_ip(request)

        if not CourseView.objects.filter(course=course, ip_address=ip_address).exists():
            CourseView.objects.create(course=course, ip_address=ip_address)

        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        return Course.objects.annotate(
            average_rating=Round(Avg('grades__rating') * 10) / 10
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
    

class ReviewLikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        comment = Review.objects.get(id=comment_id)
        like, created = ReviewLike.objects.get_or_create(user=request.user, review=comment)
        if not created:
            like.delete()
            return Response({"detail": "Like removed"}, status=status.HTTP_200_OK)
        return Response({"detail": "Like added"}, status=status.HTTP_201_CREATED)


class RatingAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = RatingSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        course_id = request.data.get('course')
        if not course_id:
            return Response({"error": "Course ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            rating = Rating.objects.get(user=request.user, course_id=course_id)
        except Rating.DoesNotExist:
            return Response({"error": "You have not rated this course yet."}, status=status.HTTP_404_NOT_FOUND)

        serializer = RatingSerializer(rating, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class FeedbackFormCreateAPIView(CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [AllowAny]

