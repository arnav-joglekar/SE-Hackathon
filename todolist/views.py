from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'todolist/todolist.html')

def assignments(request):
    return render(request, 'assignments.html')

def selfstudy(request):
    return render(request, 'selfstudy.html')