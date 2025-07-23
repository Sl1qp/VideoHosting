from django.contrib.auth import get_user_model
from django.db import models, transaction
from rest_framework import generics, views, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Video, Like
from .serializers import VideoSerializer, StatisticsSerializer
from django.db.models import F, OuterRef, Subquery, Sum
from django.core.exceptions import PermissionDenied
from .permissions import IsOwnerOrPublishedOrStaff, IsAdminUserOnly
from django.db import transaction, IntegrityError
from rest_framework.exceptions import ValidationError

User = get_user_model()


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class VideoDetailView(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsOwnerOrPublishedOrStaff]
    lookup_url_kwarg = "video_id"
    lookup_field = "id"

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                return Video.objects.all()
            return Video.objects.filter(is_published=True) | Video.objects.filter(owner=user)
        return Video.objects.filter(is_published=True)


class VideoListView(generics.ListAPIView):
    serializer_class = VideoSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsOwnerOrPublishedOrStaff]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                return Video.objects.all()
            return Video.objects.filter(is_published=True) | Video.objects.filter(owner=user)
        return Video.objects.filter(is_published=True)


class LikeToggleView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, video_id):
        video = generics.get_object_or_404(Video, id=video_id)
        if not video.is_published:
            raise PermissionDenied("Видео не опубликовано")

        try:
            with transaction.atomic():
                like, created = Like.objects.select_for_update().get_or_create(
                    video=video, user=request.user
                )
                if created:
                    video.total_likes = F("total_likes") + 1
                    video.save(update_fields=["total_likes"])
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "Вы уже поставили лайк"}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({"error": "Вы уже поставили лайк"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, video_id):
        video = generics.get_object_or_404(Video, id=video_id)
        if not video.is_published:
            raise PermissionDenied("Видео не опубликовано")

        try:
            with transaction.atomic():
                like = Like.objects.select_for_update().get(video=video, user=request.user)
                like.delete()
                video.total_likes = F("total_likes") - 1
                video.save(update_fields=["total_likes"])
                return Response(status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({"error": "Лайк не найден"}, status=status.HTTP_404_NOT_FOUND)


class PublishedVideoIdsView(views.APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        ids = Video.objects.filter(is_published=True).values_list("id", flat=True)
        return Response({"ids": list(ids)}, status=status.HTTP_200_OK)


class StatisticsSubqueryView(views.APIView):
    permission_classes = [IsAdminUserOnly]

    def get(self, request):
        subquery = Video.objects.filter(
            is_published=True,
            owner=OuterRef("pk"),
        ).values("owner").annotate(
            likes_sum=Sum("total_likes")
        ).order_by().values("likes_sum")[:1]

        users = User.objects.annotate(
            likes_sum=Subquery(subquery, output_field=models.IntegerField())
        ).order_by("-likes_sum")

        serializer = StatisticsSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StatisticsGroupByView(views.APIView):
    permission_classes = [IsAdminUserOnly]

    def get(self, request):
        from django.db.models import Sum

        users = User.objects.filter(
            videos__is_published=True
        ).annotate(
            likes_sum=Sum("videos__total_likes")
        ).filter(likes_sum__isnull=False).order_by("-likes_sum")

        serializer = StatisticsSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
