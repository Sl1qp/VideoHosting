from django.urls import path
from .views import (
    VideoDetailView,
    VideoListView,
    LikeToggleView,
    PublishedVideoIdsView,
    StatisticsSubqueryView,
    StatisticsGroupByView,
)

urlpatterns = [
    path("", VideoListView.as_view(), name="video-list"),
    path("<int:video_id>/", VideoDetailView.as_view(), name="video-detail"),
    path("<int:video_id>/likes/", LikeToggleView.as_view(), name="like-toggle"),
    path("ids/", PublishedVideoIdsView.as_view(), name="published-video-ids"),
    path("statistics-subquery/", StatisticsSubqueryView.as_view(), name="statistics-subquery"),
    path("statistics-group-by/", StatisticsGroupByView.as_view(), name="statistics-group-by"),
]
