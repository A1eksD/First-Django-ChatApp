from datetime import date
from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Message, Chat, newUser

        
class ChatTest(TestCase):
    
    def test_chatpage(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', password='testuser')
        self.client.login(username='testuser', password='testuser')

        response = self.client.get('/chat/')
        self.assertEqual( response.status_code, 200)
        
        
class ChatModelTest(TestCase): 
    '''
        Testet, ob ein Chat-Objekt korrekt erstellt wird.
    '''
    def test_create_chat(self):
        chat = Chat.objects.create(create_at=date.today())
        self.assertEqual(chat.create_at, date.today())


class MessageModelTest(TestCase):
    '''
        Erstellt zwei Benutzer und ein Chat-Objekt, das für die Tests benötigt wird.
    '''
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(username='user1', password='testpass123')
        self.user2 = get_user_model().objects.create_user(username='user2', password='testpass123')
        self.chat = Chat.objects.create(create_at=date.today())

    '''
        Testet, ob ein Message-Objekt korrekt erstellt wird und die Attribute korrekt gesetzt sind.
    '''
    def test_create_message(self):
        message = Message.objects.create(
            text="Hello, World!",
            create_at=date.today(),
            chat=self.chat,
            author=self.user1,
            receiver=self.user2
        )
        self.assertEqual(message.text, "Hello, World!")
        self.assertEqual(message.create_at, date.today())
        self.assertEqual(message.chat, self.chat)
        self.assertEqual(message.author, self.user1)
        self.assertEqual(message.receiver, self.user2)

    '''
        Testet die Beziehung zwischen Chat und Message und überprüft, ob eine Nachricht in den Nachrichten des entsprechenden Chats enthalten ist.
    '''
    def test_chat_relationship(self):
        message = Message.objects.create(
            text="Hello, Chat!",
            create_at=date.today(),
            chat=self.chat,
            author=self.user1,
            receiver=self.user2
        )
        self.assertIn(message, self.chat.chat_message_set.all())


class newUserModelTest(TestCase):

    '''
        Testet, ob ein newUser-Objekt korrekt erstellt wird und die Attribute korrekt gesetzt sind.
    '''
    def test_create_new_user(self):
        new_user = newUser.objects.create(
            name="Test User",
            email="testuser@example.com",
            password1="password123",
            password2="password123"
        )
        self.assertEqual(new_user.name, "Test User")
        self.assertEqual(new_user.email, "testuser@example.com")
        self.assertEqual(new_user.password1, "password123")
        self.assertEqual(new_user.password2, "password123")
        
     
        
class IndexViewTest(TestCase):

    '''
        Diese Methode richtet die Testumgebung ein, indem sie einen Client, einen Benutzer und einen Chat erstellt.
    '''
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass123')
        self.chat = Chat.objects.create(create_at='2023-01-01')
        self.client.login(username='testuser', password='testpass123')
        
    '''
        Testet, ob ein nicht eingeloggter Benutzer zur Login-Seite weitergeleitet wird, wenn er versucht, die index View aufzurufen.
    '''    
    def test_index_view_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, '/login/?next=/chat/')

    '''
        Testet, ob ein eingeloggter Benutzer die index View korrekt aufrufen kann und die erwartete HTML-Seite zurückgegeben wird.
    '''
    def test_index_view_get_request(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/index.html')

    '''
        Testet, ob eine POST-Anfrage an die index View korrekt verarbeitet wird, eine Nachricht erstellt wird und die erwartete JSON-Antwort zurückgegeben wird.
    '''
    def test_index_view_post_request(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('index'), {'textMessage': 'Hello, World!'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello, World!')

        # Check if the message was created
        message = Message.objects.get(text='Hello, World!')
        self.assertEqual(message.chat, self.chat)
        self.assertEqual(message.author, self.user)
        self.assertEqual(message.receiver, self.user)

    '''
        Testet, ob eine Nachricht korrekt in der Datenbank erstellt wird, wenn eine POST-Anfrage an die index View gesendet wird.
    '''
    def test_index_view_message_creation(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('index'), {'textMessage': 'Test message'})
        self.assertEqual(response.status_code, 200)

        message = Message.objects.get(text='Test message')
        self.assertEqual(message.text, 'Test message')
        self.assertEqual(message.chat, self.chat)
        self.assertEqual(message.author, self.user)
        self.assertEqual(message.receiver, self.user)
        
        
class LoginViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login_view')
        self.chat_url = reverse('index')
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_valid_user(self):
        # Teste den Login mit gültigen Daten
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpassword', 'redirect': '/chat/'})
        self.assertRedirects(response, self.chat_url)

    def test_login_invalid_user(self):
        # Teste den Login mit ungültigen Daten
        response = self.client.post(self.login_url, {'username': 'invaliduser', 'password': 'wrongpassword', 'redirect': '/chat/'})
        self.assertTemplateUsed(response, 'auth/login.html')
        self.assertTrue(response.context['wrongData'])

    def test_login_redirect(self):
        # Teste, ob nach dem Login eine Weiterleitung erfolgt
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpassword', 'redirect': '/chat/'})
        self.assertRedirects(response, self.chat_url)

    def test_login_view_get(self):
        # Teste den GET-Request auf die Login-Seite
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')
        
        
class RegisterViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register_view')
        self.chat_url = reverse('index')

    def test_register_valid_user(self):
        # Teste die Registrierung mit gültigen Daten
        response = self.client.post(self.register_url, {
            'registerName': 'testuser',
            'registerEmail': 'test@example.com',
            'registerPassword1': 'testpassword',
            'registerPassword2': 'testpassword',
            'next': '/chat/'
        })
        self.assertRedirects(response, self.chat_url)

        # Überprüfe, ob der Benutzer tatsächlich erstellt wurde
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_password_mismatch(self):
        # Teste die Registrierung mit Passwörtern, die nicht übereinstimmen
        response = self.client.post(self.register_url, {
            'registerName': 'testuser',
            'registerEmail': 'test@example.com',
            'registerPassword1': 'testpassword1',
            'registerPassword2': 'testpassword2',
            'next': '/chat/'
        })
        self.assertTemplateUsed(response, 'auth/register.html')
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], 'Passwords do not match.')

        # Überprüfe, ob der Benutzer nicht erstellt wurde
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_register_exception_handling(self):
        # Teste die Behandlung von Ausnahmen während der Registrierung
        # Hier könnte man z.B. einen Test mit ungültigen Daten oder anderen Fehlern ergänzen
        pass  # Hier müsste entsprechender Testcode eingefügt werden

    def test_register_view_get(self):
        # Teste den GET-Request auf die Registrierungsseite
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/register.html')