from django.db import models
from datetime import date
from django.conf import settings


class Chat(models.Model):
    create_at = models.DateField(default=date.today)


class Message(models.Model):
    text = models.CharField(max_length=500)
    create_at = models.DateField(default=date.today)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_message_set', default=None, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='auther_message_set')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiverer_message_set')


class newUser(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=80)
    password1 = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)