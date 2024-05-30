from django.contrib import admin
from .models import Chat, Message

class ChatAdmin(admin.ModelAdmin):
    filter_horizontal = ('users',)

admin.site.register(Chat, ChatAdmin)
admin.site.register(Message)
