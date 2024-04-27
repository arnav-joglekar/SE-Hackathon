import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm,UserProfileForm
from .models import UserProfile

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
                messages.success(request, 'Account not created successfully')
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

def userdetails(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('home')
    else:
        form = UserProfileForm()

    return render(request, 'accounts/createprofile.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('accounts:login') 