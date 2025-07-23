from django.utils import timezone
from django.db import transaction

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "videohosting.settings")  # <- Укажите путь к settings.py
django.setup()

from videos.models import Video
from django.contrib.auth import get_user_model
User = get_user_model()

def create_users_and_videos():
    with transaction.atomic():
        users = [User(
            username=f"user_{i}",
            password="password",
            email=f"user_{i}@example.com"
        ) for i in range(10_000)]
        User.objects.bulk_create(users)
        print("Пользователи созданы")

        created_users = User.objects.filter(username__startswith="user_").order_by("username")
        user_list = list(created_users)
        print("Пользователи загружены из БД")

        videos = []
        for i in range(100_000):
            user_index = i // 10
            user = user_list[user_index]
            video = Video(
                owner=user,
                name=f"Video {i}",
                is_published=True,
                total_likes=0,
                created_at=timezone.now()
            )
            videos.append(video)
            if len(videos) >= 1000:
                Video.objects.bulk_create(videos)
                videos.clear()

        if videos:
            Video.objects.bulk_create(videos)

    print("10_000 пользователей и 100_000 видео созданы")


if __name__ == "__main__":
    create_users_and_videos()