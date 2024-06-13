from mailbox import Message
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Message, Chat
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required



@login_required(login_url='/login/') # man leitet automatisch zu /login/ weiter, wenn man nicht eingeloggt ist

# Create your views here.
def index(request):
    if request.method == 'POST':
        print("Received date " + request.POST['textMessage'])
        # vergebe immer den chat mit id=1 an die message
        myChats = Chat.objects.get(id=1)
        # erstelle gleichzitig ein neues textObject
        Message.objects.create(text=request.POST['textMessage'], chat=myChats, author=request.user, receiver=request.user  )
    
    chatMessages = Message.objects.filter(chat__id=1) #chat__id=1  ==  syntax um auf chat mit der id 1 zuzugreifen

    return render(request, 'chat/index.html', {'messages': chatMessages})


def login_view(request):
    redirect = request.GET.get('next', '/chat/') #weiterleitung
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        print('user ' , user) # check user angaben
        if user:
            login(request, user) # überprüfe user in der datenbank
            return HttpResponseRedirect(request.POST.get('redirect', '/chat/')) # weiterleitung
        else:
            return render(request, 'auth/login.html', {'wrongData': True, 'redirect': redirect}) # return fehler, wenn was nicht passt
    return render(request, 'auth/login.html', {'redirect': redirect})