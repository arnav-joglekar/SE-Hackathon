from django.shortcuts import render
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile,User
from django.shortcuts import redirect, get_object_or_404
from .models import FriendRequest

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

def send_message(request):
    if request.method == 'POST':
        recipient_username = request.POST.get('recipient')
        recipient = User.objects.get(username=recipient_username)
        # Perform any additional logic here, such as saving the message to the database
        messages.success(request, f"Message sent to {recipient_username}")
        return redirect('accounts:profile')  # Redirect back to the user's profile
    else:
        # Handle GET requests or invalid form submissions
        messages.error(request, "Invalid request")
        return redirect('accounts:profile')