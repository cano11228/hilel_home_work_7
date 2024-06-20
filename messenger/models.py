from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Chat(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name='chats')

    def __str__(self):
        return self.name

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}: {self.content[:20]}'

    def can_edit_message(self, user):
        return self.author == user or user.is_superuser

    def can_delete_message(self, user):
        if user.is_superuser:
            return True

    class Meta:
        permissions = [
            ('can_edit_message', 'Can edit message'),
            ('can_delete_message', 'Can delete message')
        ]

class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='status')
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - {"Online" if self.is_online else "Offline"}'