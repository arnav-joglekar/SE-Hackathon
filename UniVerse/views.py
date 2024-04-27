import requests
from django.shortcuts import render, redirect

def home(request):
    return render(request, 'base/base.html')

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')