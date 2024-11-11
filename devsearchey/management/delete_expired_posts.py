from datetime import timedelta, timezone
from django.core.management.base import BaseCommand
from devsearchey.models import ForumPost

class Command(BaseCommand):
    help = 'Delete expired forum posts created by SneakyUser'

    def handle(self, *args, **kwargs):
        expired_posts = ForumPost.objects.filter(user__username='SneakyUser', created_at__lt=timezone.now() - timedelta(hours=12))
        expired_posts.delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted expired posts'))