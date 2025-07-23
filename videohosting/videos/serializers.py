from rest_framework import serializers
from .models import Video, VideoFile, Like


class VideoFileSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = VideoFile
        fields = ["quality", "file"]

    def get_file(self, obj):
        return obj.file.url


class VideoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    video_files = VideoFileSerializer(many=True, read_only=True)
    is_published = serializers.ReadOnlyField()

    class Meta:
        model = Video
        fields = [
            "id",
            "name",
            "total_likes",
            "created_at",
            "is_published",
            "owner",
            "video_files",
        ]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "video", "user"]
        read_only_fields = ["id"]

    def validate(self, data):
        video = data["video"]
        user = data["user"]
        if Like.objects.filter(video=video, user=user).exists():
            raise serializers.ValidationError("Вы уже поставили лайк на это видео.")
        return data


class StatisticsSerializer(serializers.Serializer):
    username = serializers.CharField()
    likes_sum = serializers.IntegerField()
