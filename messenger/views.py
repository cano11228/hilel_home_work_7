from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from .forms import MessageForm

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


@login_required
def delete_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.user == message.author:
        message.delete()
    return redirect('chat_detail', pk=message.chat.pk)
