from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Course, Review, Rating
from .utils import save_rating_and_status
from .serializers import CourseCreateSerializer, CourseDetailSerializer, CourseListSerializer, ReviewCreateSerializer, RatingSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


class CourseCreateAPIView(CreateAPIView):
    serializer_class = CourseCreateSerializer
    permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]


class CourseListAPIView(ListAPIView):
    serializer_class = CourseListSerializer
    permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return save_rating_and_status()


class CourseDetailAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]


    def get_queryset(self):
        return save_rating_and_status()
        



class ReviewCreateAPIView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]


class ReviewDeleteAPIView(DestroyAPIView):
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response(
            {"detail": "Review deleted successfully."}, 
            status=status.HTTP_200_OK
        )




class RatingCreateAPIView(CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]


class RatingUpdateAPIView(UpdateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]


class RatingDeleteAPIView(DestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

