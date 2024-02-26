from django.shortcuts import render,redirect
from .models import Room,Topic,Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
'''rooms = [
    {
        'id' : 1,
        'name' : 'Learn python with me'
    },
    {
        'id' : 2,
        'name' : 'Django Developers'
    },
    {
        'id' : 3,
        'name' : 'Web developers army'
    },
]'''

def home(request):
    q = request.GET.get('q') if request.GET.get('q')!=None  else ''

    rooms=Room.objects.all().filter(Q(topic__name__icontains=q)|
                                    Q(name__icontains=q) |
                                    Q(host__username__icontains=q)
                                    )
    
    roommsg = Message.objects.filter(Q(room__topic__name__icontains =q))

    room_count=rooms.count()
    topics=Topic.objects.all()

    context={ 'rooms' : rooms ,'topics' : topics , 'room_count' : room_count , 'roommsg' : roommsg }
    return render(request,'hotel/home.html',context)



def profileview(request,pk):
    roommsg= Message.objects.all().filter(user_id =pk)
    room = Room.objects.all().filter(host_id=pk)
    user = roommsg.first()
    topics= Topic.objects.all().filter()
    context ={'roommsg' : roommsg,'room' : room ,'user':user,'topics' : topics}

  
    return render(request,'hotel/profile.html',context)



def room(request,pk):
    room = Room.objects.get(id = pk)
    roommsg = room.message_set.all().order_by('-created')
    participant = room.participants.all()
    context = { 'room' : room , 'roommsg' : roommsg, 'participant' : participant}
    if request.method == 'POST':
        nmsg = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('comments')

        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    
    return render(request,'hotel/room.html',context)



@login_required(login_url='loginp')
def createroom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room =form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')
    context = { 'form' : form }
    return render(request,'hotel/create_room.html',context)



@login_required(login_url='loginp')
def updateroom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("Your are not allowed here!!!")
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid:
            form.save()
            return redirect('home')
        
    context = { 'form' : form }
    return render(request,'hotel/create_room.html',context)



@login_required(login_url='loginp')
def deleteroom(request, pk):
    room = Room.objects.get(id = pk)
    if request.user != room.host:
        return HttpResponse("Your are not allowed here!!!")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(request,'hotel/del.html',{'obj':room})



def loginpage(request):
    
    if request.user.is_authenticated:
        return redirect('home')

    page = 'login'
    context = { 'page': page }

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist.")

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "Invalid Username or Password.")
            
    return render(request,'hotel/log_reg.html',context)





def logoutpage(request):
    logout(request)
    return redirect('home') 


def registerpage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "Registration was unsucessfull")
        
    return render(request,'hotel/log_reg.html',{ 'form' : form })


@login_required(login_url='loginp')
def deletemsg(request, pk):
    message = Message.objects.get(id = pk)
    if request.user != message.user:
        return HttpResponse("Your are not allowed here!!!")
    else:
        if request.method == 'POST':
            message.delete()
            return redirect('home')    
        return render(request,'hotel/del.html',{'obj':message})
