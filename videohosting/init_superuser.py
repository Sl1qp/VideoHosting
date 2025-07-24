import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "videohosting.settings")
django.setup()

User = get_user_model()

admin_name = os.getenv("ADMIN_NAME")
admin_email = os.getenv("ADMIN_EMAIL")
admin_pass = os.getenv("ADMIN_PASS")

if admin_name and admin_email and admin_pass:
    if not User.objects.filter(username=admin_name).exists():
        User.objects.create_superuser(
            username=admin_name,
            email=admin_email,
            password=admin_pass
        )