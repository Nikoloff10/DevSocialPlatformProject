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




