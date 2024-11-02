from django.conf import settings
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(default='no bio...')
    avatar = models.ImageField(default='avatars/default.jpg', upload_to='avatars/')
    github = models.URLField(blank=True)
    website = models.URLField(blank=True)


    def __str__(self):
        return str(self.user.username)


class JobPost(models.Model):
    JOB_SEEKING = 'seeking'
    JOB_OFFERING = 'offering'
    POST_TYPE_CHOICES = [
        (JOB_SEEKING, 'Job Seeking'),
        (JOB_OFFERING, 'Job Offering'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=8, choices=POST_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"