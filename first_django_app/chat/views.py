from mailbox import Message
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import Message, Chat
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers





@login_required(login_url='/login/') # man leitet automatisch zu /login/ weiter, wenn man nicht eingeloggt ist

# Create your views here.
def index(request):
    if request.method == 'POST':
        print("Received date " + request.POST['textMessage'])
        # vergebe immer den chat mit id=1 an die message
        myChats = Chat.objects.get(id=1)
        # erstelle gleichzitig ein neues textObject
        new_message = Message.objects.create(text=request.POST['textMessage'], chat=myChats, author=request.user, receiver=request.user  )
        serialized_obj = serializers.serialize('json', [ new_message, ]) # wandel die message in ein array um
        return JsonResponse(serialized_obj[1:-1], safe=False) # gib das json als wtring wieder / [1:-1] entfernt die [] und returnt einen reinen json und kein string
    chatMessages = Message.objects.filter(chat__id=1) #chat__id=1  ==  syntax um auf chat mit der id 1 zuzugreifen

    return render(request, 'chat/index.html', {'messages': chatMessages})


def login_view(request):
    redirect = request.GET.get('next', '/chat/') #weiterleitung (next im link nicht vorhaned, deshalb chat als ausweichmöglichkeit)
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        print('user ' , user) # check user angaben
        if user:
            login(request, user) # überprüfe user in der datenbank
            return HttpResponseRedirect(request.POST.get('redirect', '/chat/')) # weiterleitung
        else:
            return render(request, 'auth/login.html', {'wrongData': True, 'redirect': redirect}) # return fehler, wenn was nicht passt
    return render(request, 'auth/login.html', {'redirect': redirect})


def register_view(request):
    redirect = request.GET.get('next', '/chat/')
    if request.method == 'POST':
        # lese die daten aus
        username = request.POST.get('registerName')
        email = request.POST.get('registerEmail')
        password1 = request.POST.get('registerPassword1')
        password2 = request.POST.get('registerPassword2')

        # überprüfe ob pw's gleich sind
        if password1 != password2: 
            return render(request, 'auth/register.html', {'error': 'Passwords do not match.', 'redirect': redirect})

        try:
            user = User.objects.create_user(username, email, password1) #lege den user mit create_user an
            login(request, user) # überprüfe user in der datenbank
            return HttpResponseRedirect(redirect) # weiterleitung
        except Exception as e:
            # Handle other registration errors
            print(f"Registration error: {e}")
            return render(request, 'auth/register.html', {'error': str(e)})  # zeige error

    return render(request, 'auth/register.html', {'redirect': redirect})


