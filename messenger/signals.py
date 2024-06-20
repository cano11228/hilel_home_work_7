from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from .models import Message, UserStatus
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Message)
def log_message_sent(sender, instance, created, **kwargs):
    if created:
        # Записати лог про відправлене повідомлення
        logger.info(f'Message sent by {instance.author} to chat {instance.chat.id}: {instance.content}')

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    UserStatus.objects.update_or_create(user=user, defaults={'is_online': True, 'last_seen': timezone.now()})

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    UserStatus.objects.update_or_create(user=user, defaults={'is_online': False, 'last_seen': timezone.now()})