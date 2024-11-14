from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ForumPost, Profile
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Add logging to pre_delete and post_delete signals for ForumPost
@receiver(pre_delete, sender=ForumPost)
def log_pre_delete(sender, instance, **kwargs):
    logger.info(f'Pre-delete signal received for post: {instance.title} (ID: {instance.id})')

@receiver(post_delete, sender=ForumPost)
def log_post_delete(sender, instance, **kwargs):
    logger.info(f'Post-delete signal received for post: {instance.title} (ID: {instance.id})')