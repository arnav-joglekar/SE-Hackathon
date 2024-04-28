import requests
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm,UserProfileForm
from .models import UserProfile
from connections.models import FriendRequest
from accounts.models import Domain

def index(request):
    return render(request, 'base/base.html')

def signup(request):
    form = CreateUserForm()

    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST) 
            if form.is_valid():
                user = form.save()
                messages.success(request, 'Account created successfully')
                return redirect('accounts:login')
            else:
                messages.warning(request, 'Account not created successfully')
        context = {'form': form}  
        return render(request, 'accounts/signup.html', context)
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:  
            login(request, user)
            if not hasattr(user, 'userprofile'):
                return redirect('accounts:userdetails')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid login details. Check your username and password.')

    return render(request, 'accounts/login.html')

@login_required(login_url='accounts:login')
def userdetails(request):
    if request.method == 'POST':
        if not UserProfile.objects.filter(user=request.user).exists():
            form = UserProfileForm(request.POST)
            print("hi")
            print(form.errors)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                form.save_m2m()
                return redirect('home')
    
    form = UserProfileForm()
    domain_choices = Domain.objects.all()
    context = {
        'form': form,
        'domain_choices': domain_choices,
    }
    return render(request, 'accounts/createprofile.html', context)

@login_required(login_url='accounts:login')
def profile(request):
    user = request.user
    friend_requests = FriendRequest.objects.filter(receiver=user)  # Requests sent by the user
    user_profile = UserProfile.objects.get(user=user)
    friends = user_profile.friends.all()
    context = {
        'user': user,
        'friend_requests': friend_requests,
        'friends': friends,
    }
    return render(request, 'accounts/profile.html', context)

@login_required(login_url='accounts:login')
def accept_decline_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            # Accept the friend request
            friend_request.status = 'accepted'
            friend_request.save()
            sender_profile = UserProfile.objects.get(user=friend_request.sender)
            receiver_profile = UserProfile.objects.get(user=friend_request.receiver)
            sender_profile.friends.add(friend_request.receiver)
            receiver_profile.friends.add(friend_request.sender)
            friend_request.delete()
        elif action == 'decline':
            # Decline the friend request
            friend_request.status = 'declined'
            friend_request.save()
            friend_request.delete()
        return redirect('accounts:profile')
    
    return redirect('accounts:profile')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('accounts:login') 