from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Room

@login_required
def rooms(request):
    rooms=Room.objects.all()
    context= {
        'rooms':rooms,
    }
    return render(request,'room/rooms.html',context)

@login_required
def room(request, room_name):
    username = request.GET.get('username', 'Anonymous')
    #room=Room.objects.get(slug=slug)
    context= {
        'room_name':room_name,
        'username':username,
    }
    return render(request,'room/room.html',context)