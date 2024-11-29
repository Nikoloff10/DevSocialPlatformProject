from django.db.models.signals import m2m_changed, post_save, pre_delete, post_delete
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


@receiver(pre_delete, sender=ForumPost)
def log_pre_delete(sender, instance, **kwargs):
    logger.info(f'Pre-delete signal received for post: {instance.title} (ID: {instance.id})')

@receiver(post_delete, sender=ForumPost)
def log_post_delete(sender, instance, **kwargs):
    logger.info(f'Post-delete signal received for post: {instance.title} (ID: {instance.id})')

STAFF_GROUPS = ['Moderators', 'Support']

@receiver(m2m_changed, sender=User.groups.through)
def update_is_staff_status(sender, instance, action, pk_set, **kwargs):
    if action in ['post_add', 'post_remove']:
        
        current_groups = instance.groups.values_list('name', flat=True)
        
        
        if any(group in STAFF_GROUPS for group in current_groups):
            if not instance.is_staff:
                instance.is_staff = True
                instance.save()
        else:
            if instance.is_staff:
                instance.is_staff = False
                instance.save()