from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from .models import Chat, Message
from django.contrib import messages


class UserIsAuthorMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            return redirect('chat_detail', pk=obj.chat.pk)
        return super().dispatch(request, *args, **kwargs)

class ChatParticipantsMixin:
    def dispatch(self, request, *args, **kwargs):
        chat = get_object_or_404(Chat, pk=kwargs['pk'])
        if request.user not in chat.users.all():
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class SuperuserMessageMixin:
    def form_valid(self, form):
        response = super().form_valid(form)
        chat = self.object.chat
        if chat.users.filter(is_superuser=True).exists():
            messages.success(self.request, 'Ви успішно надіслали повідомлення суперюзеру')
        return response


class ChatAccessMixin:
    def get_chat(self, pk):
        return get_object_or_404(Chat, pk=pk)

    def check_chat_access(self, request, chat):
        if request.user not in chat.users.all():
            raise PermissionDenied

class MessageAccessMixin:
    def get_message(self, pk):
        return get_object_or_404(Message, pk=pk)

    def check_message_author(self, request, message):
        if request.user != message.author:
            raise PermissionDenied

class SuperuserRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class FormValidMixin:
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class MessageAuthorRequiredMixin(MessageAccessMixin):
    def dispatch(self, request, pk, *args, **kwargs):
        message = self.get_message(pk)
        self.check_message_author(request, message)
        return super().dispatch(request, pk, *args, **kwargs)

class ChatUserRequiredMixin(ChatAccessMixin):
    def dispatch(self, request, pk, *args, **kwargs):
        chat = self.get_chat(pk)
        self.check_chat_access(request, chat)
        return super().dispatch(request, pk, *args, **kwargs)

class ChatRequiredMixin(ChatAccessMixin):
    def dispatch(self, request, pk, *args, **kwargs):
        chat = self.get_chat(pk)
        if chat.users.filter(pk=request.user.pk).exists():
            return super().dispatch(request, pk, *args, **kwargs)
        else:
            return redirect('home')

class MessageRequiredMixin(MessageAccessMixin):
    def dispatch(self, request, pk, *args, **kwargs):
        message = self.get_message(pk)
        if request.user == message.author or request.user.is_superuser:
            return super().dispatch(request, pk, *args, **kwargs)
        else:
            raise PermissionDenied
