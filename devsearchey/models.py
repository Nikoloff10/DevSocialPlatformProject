from datetime import timedelta, timezone
from django.conf import settings

from django.db import models




class JobPost(models.Model):
    JOB_SEEKING = 'seeking'
    JOB_OFFERING = 'offering'
    POST_TYPE_CHOICES = [
        (JOB_SEEKING, 'Job Seeking'),
        (JOB_OFFERING, 'Job Offering'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_posts')
    post_type = models.CharField(max_length=8, choices=POST_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    bookmark_count = models.PositiveIntegerField(default=0)
    bookmarked_by = models.ManyToManyField('Profile', related_name='bookmarked_job_posts', blank=True)
    reference_number = models.CharField(max_length=10, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.post_type == self.JOB_OFFERING and not self.reference_number:
            self.reference_number = f"REF{self.pk:06d}"
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(default='no bio...')
    avatar = models.ImageField(default='avatars/default.jpg', upload_to='avatars/')
    github = models.URLField(blank=True)
    website = models.URLField(blank=True)
    bookmarked_posts = models.ManyToManyField(JobPost, related_name='bookmarked_by_profiles', blank=True)

    def __str__(self):
        return str(self.user.username)



class ForumPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_forum_posts', blank=True)

    def __str__(self):
        return self.title

    def should_expire(self):
        if self.user and self.user.username == 'SneakyUser':
            return timezone.now() > self.created_at + timedelta(hours=12)
        return False

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    forum_post = models.ForeignKey(ForumPost, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments', blank=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.forum_post.title}"
