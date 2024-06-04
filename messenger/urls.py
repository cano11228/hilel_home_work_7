from django.urls import path
from . import views

urlpatterns = [
    path('chat/<int:pk>/', views.chat_detail, name='chat_detail'),
    path('chats/', views.chat_list, name='chat_list'),  # Новий маршрут
    path('message/<int:pk>/edit/', views.edit_message, name='edit_message'),
    path('message/<int:pk>/delete/', views.delete_message, name='delete_message'),
    # path('assign_can_delete_message', views.assign_can_delete_message_permission, name='assign_permission')
]

