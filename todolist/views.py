from django.shortcuts import render
from .models import Selfstudy, Assignment
from django.shortcuts import redirect
from .forms import selfstudyform, assignmentsform
import uuid
# Create your views here.
def index(request):
    return render(request, 'todolist/todolist.html')

def assignments(request):
    assignments= Assignment.objects.all()
    context = {
        'assignments': assignments
    }
    return render(request, 'todolist/assignments.html',context)

def selfstudy(request):
    selfstudy=Selfstudy.objects.all()
    context = {
        'selfstudy': selfstudy
    }
    return render(request, 'todolist/selfstudy.html',context)

def create_assignments(request):
    if request.method == 'POST':
        form = assignmentsform(request.POST)

        if form.is_valid():
            form.save()
            return redirect('todolist:assignments')
    else:
        form = selfstudyform()
    return render(request, 'todolist/assignments.html')

def create_selfstudy(request):
    if request.method == 'POST':
        form = selfstudyform(request.POST)
        # hi=request.POST['name']
        # print(hi)
        print(form.errors)
        print("hello")
        if form.is_valid():
            print("hello")
            form.save()
            return redirect('todolist:selfstudy')
    else:
        form = selfstudyform()
    return render(request, 'todolist/selfstudy.html', {'form': form})

def complete_selfstudy(request, uuid):
    selfstudy = Selfstudy.objects.get(uuid=uuid)
    selfstudy.completed=True
    selfstudy.save()
    return redirect('todolist:selfstudy')