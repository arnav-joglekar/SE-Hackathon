from django.shortcuts import render
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile,User
from django.shortcuts import redirect, get_object_or_404
from .models import FriendRequest
from django.http import JsonResponse
import json
from .models import Message

# Create your views here.
def connect(request):
    students = UserProfile.objects.exclude(user=request.user)
    courses = request.GET.get('courses')
    if courses:
        students = students.filter(courses=courses)
    DEPARTMENT_YEAR_CHOICES = UserProfile.DEPARTMENT_YEAR_CHOICES  # Retrieve choices
    context = {
        'students': students,
        'DEPARTMENT_YEAR_CHOICES': DEPARTMENT_YEAR_CHOICES,  # Pass choices to template
    }
    return render(request, 'connect/connect.html', context)

@login_required
def send_friend_request(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    sender = request.user
    existing_request = FriendRequest.objects.filter(sender=sender, receiver=receiver).exists()
    print(existing_request)
    if not existing_request:
        friend_request = FriendRequest.objects.create(sender=sender, receiver=receiver)
        print('Friend Request sent') 
    return redirect('connections:connect')

def friends(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    friends = user_profile.friends.all()

    context = {
        'user': user,
        'friends': friends,
    }
    return render(request, 'connect/friends.html', context)


def chat(request, username):
    if request.method == 'POST':
        recipient_username = request.POST.get('recipient')
        recipient = User.objects.get(username=recipient_username)
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=recipient, content=content)
        return redirect('connections:chat', username=recipient_username)
    else:
        recipient = User.objects.get(username=username)
        messages_history = Message.objects.filter(sender=request.user, receiver=recipient) | Message.objects.filter(sender=recipient, receiver=request.user)
        return render(request, 'connect/chat.html', {'recipient': recipient, 'messages': messages_history})
    
def videocall(request):
    username = request.user.username
    return render(request, 'connect/meeting.html',{'username':username})