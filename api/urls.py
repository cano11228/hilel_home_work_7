from django.urls import path
from .views import ChatListView, MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView

urlpatterns = [
    path('chats/', ChatListView.as_view(), name='chat-list'),
    path('chats/<int:chat_id>/messages/', MessageListView.as_view(), name='message-list'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('messages/create/', MessageCreateView.as_view(), name='message-create'),
    path('messages/<int:pk>/edit/', MessageUpdateView.as_view(), name='message-edit'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message-delete'),
]
