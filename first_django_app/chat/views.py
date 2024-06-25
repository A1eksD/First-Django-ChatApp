from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import Message as ChatMessage, Chat
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers

@login_required(login_url='/login/')  # man leitet automatisch zu /login/ weiter, wenn man nicht eingeloggt ist
def index(request):
    if request.method == 'POST':
        print("Received data " + request.POST['textMessage'])
        # vergebe immer den Chat mit id=1 an die Message
        myChats = Chat.objects.get(id=1)
        # erstelle gleichzeitig ein neues Text-Objekt
        new_message = ChatMessage.objects.create(
            text=request.POST['textMessage'],
            chat=myChats,
            author=request.user,
            receiver=request.user
        )
        serialized_obj = serializers.serialize('json', [new_message])
        return JsonResponse(serialized_obj[1:-1], safe=False)
    
    chatMessages = ChatMessage.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {'messages': chatMessages})

def login_view(request):
    redirect = request.GET.get('next', '/chat/')
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        print('user', user)  # check user Angaben
        if user:
            login(request, user)  # überprüfe user in der Datenbank
            return HttpResponseRedirect(request.POST.get('redirect', '/chat/'))  # Weiterleitung
        else:
            return render(request, 'auth/login.html', {'wrongData': True, 'redirect': redirect})
    return render(request, 'auth/login.html', {'redirect': redirect})

def register_view(request):
    redirect = request.GET.get('next', '/chat/')
    if request.method == 'POST':
        # lese die Daten aus
        username = request.POST.get('registerName')
        email = request.POST.get('registerEmail')
        password1 = request.POST.get('registerPassword1')
        password2 = request.POST.get('registerPassword2')

        # überprüfe ob PW's gleich sind
        if password1 != password2:
            return render(request, 'auth/register.html', {'error': 'Passwords do not match.', 'redirect': redirect})

        try:
            user = User.objects.create_user(username=username, email=email, password=password1)  # lege den User an
            login(request, user)  # logge den User ein
            return HttpResponseRedirect(redirect)  # Weiterleitung
        except Exception as e:
            # Handle other registration errors
            print(f"Registration error: {e}")
            return render(request, 'auth/register.html', {'error': str(e), 'redirect': redirect})  # zeige Fehler

    return render(request, 'auth/register.html', {'redirect': redirect})
