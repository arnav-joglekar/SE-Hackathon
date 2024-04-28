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
from accounts.models import Domain
from .models import Message

# Create your views here.
@login_required(login_url='accounts:login')
def connect(request):
    user_profiles = UserProfile.objects.exclude(user=request.user)
    current_user_friends_ids = request.user.friends.values_list('user_id', flat=True)
    user_profiles = user_profiles.exclude(user__id__in=current_user_friends_ids)

    all_domains = set()
    for profile in user_profiles:
        all_domains.update(profile.domains.all())

    courses = request.GET.get('courses')
    domains = request.GET.get('domains')
    search_query = request.GET.get('search')  # New: Get search query
    availability = request.GET.get('availability')
    
    if search_query:
        user_profiles = user_profiles.filter(user__username__icontains=search_query)  # New: Filter by username
    
    if courses:
        user_profiles = user_profiles.filter(courses=courses)
    
    if domains:
        user_profiles = user_profiles.filter(domains__name=domains)

    if availability:  # Filter by availability if provided
        user_profiles = user_profiles.filter(availability=availability)
    
    
    DEPARTMENT_YEAR_CHOICES = UserProfile.DEPARTMENT_YEAR_CHOICES  
    
    # Check for pending friend requests and friendships
    current_user = request.user
    for profile in user_profiles:
        # Check if there's a pending friend request or if they are already friends
        profile.has_pending_request = FriendRequest.objects.filter(sender=current_user, receiver=profile.user).exists()
        profile.is_friend = current_user.friends.filter(user_id=profile.user.id).exists()

    context = {
        'students': user_profiles,
        'domains_choices': all_domains,
        'DEPARTMENT_YEAR_CHOICES': DEPARTMENT_YEAR_CHOICES,  
        'userprofile': request.user.userprofile,
    }
    return render(request, 'connect/connect.html', context)


@login_required(login_url='accounts:login')
def send_friend_request(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    sender = request.user
    existing_request = FriendRequest.objects.filter(sender=sender, receiver=receiver).exists()
    if not existing_request:
        friend_request = FriendRequest.objects.create(sender=sender, receiver=receiver)
        print('Friend Request sent') 
    return redirect('connections:connect')

@login_required(login_url='accounts:login')
def friends(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    friends = user_profile.friends.all()

    context = {
        'user': user,
        'friends': friends,
    }
    return render(request, 'connect/friends.html', context)

@login_required(login_url='accounts:login')
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

@login_required(login_url='accounts:login')
def videocall(request):
    username = request.user.username
    return render(request, 'connect/meeting.html',{'username':username})

@login_required(login_url='accounts:login')
def joinmeet(request):
    if request.method=='POST':
        rid=request.POST['roomID']
        return redirect("/connect/meeting?roomID="+rid)
    return render(request,'connect/joinmeet.html')