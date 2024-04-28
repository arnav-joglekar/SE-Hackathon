from django.shortcuts import render
from .models import Selfstudy, Assignment
from django.shortcuts import redirect
from .forms import selfstudyform, assignmentsform
from datetime import datetime
import uuid
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='accounts:login')
def index(request):
    return render(request, 'todolist/todolist.html')

@login_required(login_url='accounts:login')
def assignments(request):
    assignments= Assignment.objects.all()
    currentTime = datetime.now().replace(tzinfo=None)
    for a in assignments:
        if a.due_date is not None:
            a.is_before_due_date = a.due_date.replace(tzinfo=None) < currentTime
        else:
            a.is_before_due_date = False
    context = {
        'currentTime': currentTime,
        'assignments': assignments
    }
    return render(request, 'todolist/assignments.html',context)

@login_required(login_url='accounts:login')
def selfstudy(request):
    selfstudy=Selfstudy.objects.all()
    currentTime = datetime.now().replace(tzinfo=None)
    for s in selfstudy:
        if s.due_date is not None:
            s.is_before_due_date = s.due_date.replace(tzinfo=None) < currentTime
        else:
            s.is_before_due_date = False

    context = {
        'currentTime': currentTime,
        'selfstudy': selfstudy
    }
    return render(request, 'todolist/selfstudy.html',context)

@login_required(login_url='accounts:login')
def create_assignments(request):
    if request.method == 'POST':
        form = assignmentsform(request.POST)

        if form.is_valid():
            form.save()
            return redirect('todolist:assignments')
    else:
        form = assignmentsform()
    return render(request, 'todolist/assignments.html',{'form': form})

@login_required(login_url='accounts:login')
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

@login_required(login_url='accounts:login')
def complete_selfstudy(request, uuid):
    selfstudy = Selfstudy.objects.get(uuid=uuid)
    selfstudy.completed=True
    selfstudy.save()
    return redirect('todolist:selfstudy')

@login_required(login_url='accounts:login')
def complete_assignments(request, uuid):
    assignments = Assignment.objects.get(uuid=uuid)
    assignments.completed=True
    assignments.save()
    return redirect('todolist:assignments')

@login_required(login_url='accounts:login')
def delete_selfstudy(request, uuid):
    selfstudy = Selfstudy.objects.get(uuid=uuid)
    selfstudy.delete()
    return redirect('todolist:selfstudy')

@login_required(login_url='accounts:login')
def delete_assignments(request, uuid):
    assignments = Assignment.objects.get(uuid=uuid)
    assignments.delete()
    return redirect('todolist:assignments')







