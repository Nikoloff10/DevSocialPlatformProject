from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from devsearchey.models import ForumPost
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

@shared_task
def delete_expired_posts():
    logger.info("Starting delete_expired_posts task.")
    with transaction.atomic():
        
        expiration_time = timezone.now() - timedelta(minutes=1)  # timedelta(weeks=1) instead of timedelta(minutes=1) for real world usage
        expired_posts = ForumPost.objects.filter(
            user__username='SneakyUser',
            created_at__lt=expiration_time
        )
        count = expired_posts.count()
        logger.info(f'Found {count} expired posts to delete.')

        for post in expired_posts:
            logger.info(f'Deleting post: "{post.title}')
            post.delete()
            logger.info(f'Post "{post.title}" (ID: {post.id}) deleted.')

        logger.info(f'Successfully deleted {count} expired posts.')
    return f'Successfully deleted {count} expired posts'