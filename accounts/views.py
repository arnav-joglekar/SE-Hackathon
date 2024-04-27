import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm

def index(request):
    return render(request, 'base/base.html')

def signup(request):
    form = CreateUserForm()

    if request.user.is_authenticated:
        return redirect('base/base.html')
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
            return redirect('base/base')
        else:
            messages.error(request, 'Invalid login details. Check your username and password.')
            
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('accounts/login') 