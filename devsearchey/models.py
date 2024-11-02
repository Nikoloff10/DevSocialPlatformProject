from django.conf import settings
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(default='no bio...')
    avatar = models.ImageField(default='default.jpg', upload_to='avatars/')
    email = models.EmailField(unique=True)
    github = models.URLField(blank=True)
    website = models.URLField(blank=True)


    def __str__(self):
        return str(self.user.username)