from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Chat, Message
from .forms import MessageForm
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

User = get_user_model()

@login_required
def chat_list(request):
    chats = Chat.objects.filter(users=request.user)
    return render(request, 'messenger/chat_list.html', {'chats': chats})



@login_required
def chat_detail(request, pk):
    chat = get_object_or_404(Chat, pk=pk)
    if request.user not in chat.users.all():
        return redirect('home')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.author = request.user
            message.save()
            return redirect('chat_detail', pk=chat.pk)
    else:
        form = MessageForm()

    return render(request, 'messenger/chat_detail.html', {'chat': chat, 'form': form})

@permission_required('messenger.can_edit_message')
@login_required
def edit_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.user != message.author:
        return redirect('chat_detail', pk=message.chat.pk)

    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('chat_detail', pk=message.chat.pk)
    else:
        form = MessageForm(instance=message)

    return render(request, 'messenger/edit_message.html', {'form': form})

@permission_required('messenger.can_delete_message')
@login_required
def delete_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.user.is_superuser:
        message.delete()
    return redirect('chat_detail', pk=message.chat.pk)

    # def assign_can_delete_message_permission(request, user_id):
    #     if request.method == 'POST':
    #         selected_users = request.POST.getlist('users')
    #         content_type = ContentType.objects.get_for_model(Message)
    #
    #         can_delete_message_permission = Permission.objects.filter(
    #             codename='can_delete_message',
    #             content_type=content_type
    #         ).first()
    #
    #         for user_id in selected_users:
    #             user = User.objects.filter(id=user_id).first()
    #             if user:
    #                 user.user_permissions.add(can_delete_message_permission)
    #
    #         return redirect("assign_permission")
    #
    #     users = User.objects.all()
    #     return render(request, 'assign_can_delete_message.html', {'users': users})