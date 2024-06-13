from django.db import models
from datetime import date
from django.conf import settings

# Create your models here.


class Chat(models.Model):
    create_at = models.DateField(default=date.today)


class Message(models.Model):
    # CharField = Buchstabenfeld
    text = models.CharField(max_length=500)
    # Datumfled mit aktuellem datum drin
    create_at = models.DateField(default=date.today)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_message_set', default=None, blank=True, null=True)
    # ForeignKey = Fremdschlüssel(import des grundaubaus, [beim löschen]impord des löschens von allem was zum user gehört, 
    #   info für die datenbank zum einkategoresieren)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='auther_message_set')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiverer_message_set')


class newUser(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=80)
    password1 = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)