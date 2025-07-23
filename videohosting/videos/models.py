from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import os


class Video(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="videos"
    )
    is_published = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    total_likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class VideoFile(models.Model):
    QUALITY_CHOICES = [
        ("HD", "HD (720p)"),
        ("FHD", "FHD (1080p)"),
        ("UHD", "UHD (4K)"),
    ]

    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name="video_files"
    )
    file = models.FileField(
        upload_to="videos/",
        verbose_name="Видеофайл",
        help_text="Загрузите файл в формате MP4"
    )
    quality = models.CharField(
        max_length=3,
        choices=QUALITY_CHOICES,
        verbose_name="Качество"
    )

    def __str__(self):
        return f"{self.video.name} ({self.get_quality_display()})"

    def clean(self):
        ext = os.path.splitext(self.file.name)[1].lower()
        if ext not in [".mp4", ".mkv", ".avi"]:
            raise ValidationError("Недопустимый формат файла. Разрешены: .mp4, .mkv, .avi")


class Like(models.Model):
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="video_likes"
    )

    class Meta:
        unique_together = ["video", "user"]
        constraints = [
            models.UniqueConstraint(
                fields=["video", "user"],
                name="unique_user_video_like"
            )
        ]

    def __str__(self):
        return f"Лайк от {self.user.username} к {self.video.name}"