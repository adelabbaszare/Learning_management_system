from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    is_instructor = models.BooleanField(default=False)

    def get_image(self):
        if self.image:
            base = getattr(settings, 'WEBSITE_URL', '')
            return base + self.image.url if base else self.image.url
        return '/static/img/default-user.png'

