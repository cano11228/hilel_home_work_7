from django.urls import path
from .views import chat_list, ChatDetailView, EditMessageView, DeleteMessageView

urlpatterns = [
    path('', chat_list, name='chat_list'),
    path('chat/<int:pk>/', ChatDetailView.as_view(), name='chat_detail'),
    path('message/<int:pk>/edit/', EditMessageView.as_view(), name='edit_message'),
    path('message/<int:pk>/delete/', DeleteMessageView.as_view(), name='delete_message'),
]
