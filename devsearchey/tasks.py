from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from devsearchey.models import ForumPost
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

@shared_task
def delete_expired_posts():
    with transaction.atomic():
        # Identify posts created by SneakyUser that are older than 1 minute
        expired_posts = ForumPost.objects.filter(user__username='SneakyUser', created_at__lt=timezone.now() - timedelta(minutes=1)) # should be 1 week for production
        count = expired_posts.count()
        logger.info(f'[{timezone.now()}] Found {count} expired posts to delete.')
        
        for post in expired_posts:
            logger.info(f'[{timezone.now()}] Deleting post: {post.title} (ID: {post.id})')
            post.delete()
            logger.info(f'[{timezone.now()}] Post {post.title} (ID: {post.id}) deleted.')
        
        logger.info(f'[{timezone.now()}] Successfully deleted {count} expired posts.')
    return f'Successfully deleted {count} expired posts'