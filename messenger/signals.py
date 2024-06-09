from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Message)
def log_message_sent(sender, instance, created, **kwargs):
    if created:
        # Записати лог про відправлене повідомлення
        logger.info(f'Message sent by {instance.author} to chat {instance.chat.id}: {instance.content}')
