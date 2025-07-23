from django.contrib import admin
from .models import Video, VideoFile, Like


class VideoFileInline(admin.TabularInline):
    model = VideoFile
    extra = 1
    fields = ("file", "quality")
    verbose_name = "Видеофайл"
    verbose_name_plural = "Видеофайлы"


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "is_published", "total_likes", "created_at")
    list_filter = ("is_published", "owner")
    search_fields = ("name", "owner__username")
    inlines = [VideoFileInline]
    readonly_fields = ("created_at", "total_likes")
    fieldsets = (
        (None, {
            "fields": ("name", "owner", "is_published")
        }),
        ("Метаданные", {
            "fields": ("created_at", "total_likes")
        }),
    )


@admin.register(VideoFile)
class VideoFileAdmin(admin.ModelAdmin):
    list_display = ("video", "quality", "file")
    list_filter = ("quality", "video")
    search_fields = ("video__name",)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("video", "user")
    list_filter = ("video", "user")
    search_fields = ("video__name", "user__username")
