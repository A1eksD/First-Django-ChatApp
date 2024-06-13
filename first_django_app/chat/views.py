from mailbox import Message
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Message, Chat
from django.contrib.auth import authenticate, login


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
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        print('user ' , user) # check user angaben
        if user:
            login(request, user) # überprüfe user in der datenbank
            return HttpResponseRedirect('/chat/') # weiterleitung
        else:
            return render(request, 'auth/login.html', {'wrongData': True}) # return fehler, wenn was nicht passt
    return render(request, 'auth/login.html')