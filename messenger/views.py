# myproject/messenger/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, UpdateView, DeleteView, FormView
from .models import Chat, Message
from .forms import MessageForm
from .mixins import UserIsAuthorMixin, ChatParticipantsMixin, SuperuserMessageMixin
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def chat_list(request):
    chats = Chat.objects.filter(users=request.user)
    return render(request, 'messenger/chat_list.html', {'chats': chats})

@method_decorator(login_required, name='dispatch')
class ChatDetailView(ChatParticipantsMixin, SuperuserMessageMixin, DetailView, FormView):
    model = Chat
    template_name = 'messenger/chat_detail.html'
    context_object_name = 'chat'
    form_class = MessageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        message = form.save(commit=False)
        message.chat = self.object
        message.author = self.request.user
        message.save()
        if self.object.users.filter(is_superuser=True).exists():
            messages.success(self.request, 'Ви успішно надіслали повідомлення суперюзеру')
        return redirect('chat_detail', pk=self.object.pk)

@method_decorator(permission_required('messenger.can_edit_message'), name='dispatch')
@method_decorator(login_required, name='dispatch')
class EditMessageView(UserIsAuthorMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'messenger/edit_message.html'

    def get_success_url(self):
        return redirect('chat_detail', pk=self.object.chat.pk)

@method_decorator(permission_required('messenger.can_delete_message'), name='dispatch')
@method_decorator(login_required, name='dispatch')
class DeleteMessageView(DeleteView):
    model = Message

    def get_success_url(self):
        return redirect('chat_detail', pk=self.object.chat.pk)
